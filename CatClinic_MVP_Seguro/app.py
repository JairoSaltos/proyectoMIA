from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from safety import clasificar_mensaje


BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Clasificador de Mensajes - Clínica Veterinaria",
    page_icon="🐾",
    layout="centered",
)


@st.cache_resource
def cargar_modelo():
    modelo = joblib.load(BASE_DIR / "modelo_clasificador.pkl")
    vectorizador = joblib.load(BASE_DIR / "tfidf_vectorizer.pkl")
    return modelo, vectorizador


def guardar_en_historial(mensaje, resultado):
    st.session_state.historial.insert(
        0,
        {
            "Hora": datetime.now().strftime("%H:%M:%S"),
            "Mensaje": mensaje,
            "Categoría": resultado.categoria or "Sin clasificación",
            "Score estimado (%)": (
                f"{resultado.score * 100:.1f}" if resultado.score is not None else "N/A"
            ),
            "Revisión humana": "Sí" if resultado.requiere_revision else "No",
            "Motivo": "; ".join(resultado.motivos_revision) or "—",
        },
    )


def mostrar_resultado(resultado):
    if resultado.estado == "entrada_invalida":
        st.warning(resultado.mensaje_usuario)
        return

    if resultado.estado == "informacion_insuficiente":
        st.warning(resultado.mensaje_usuario)
        return

    st.divider()
    st.subheader("Resultado de la clasificación")

    score_texto = (
        f"{resultado.score * 100:.1f}%" if resultado.score is not None else "No disponible"
    )
    st.info(
        f"**Categoría detectada:** {resultado.categoria}  \n"
        f"**Score estimado (no calibrado):** {score_texto}"
    )

    if resultado.requiere_revision:
        st.warning(
            "⚠️ **Revisión humana requerida antes de responder.**  \n"
            + "Motivo: "
            + "; ".join(resultado.motivos_revision)
            + "."
        )
    else:
        st.success("No se activaron alertas automáticas de revisión.")

    if resultado.scores_por_categoria:
        tabla_scores = pd.DataFrame(
            {
                "Categoría": resultado.scores_por_categoria.keys(),
                "Distribución estimada (%)": [
                    valor * 100 for valor in resultado.scores_por_categoria.values()
                ],
            }
        )
        tabla_scores["Distribución estimada (%)"] = tabla_scores[
            "Distribución estimada (%)"
        ].round(2)
        tabla_scores = tabla_scores.sort_values(
            "Distribución estimada (%)", ascending=False
        )
        with st.expander("Ver distribución estimada por categoría"):
            st.dataframe(tabla_scores, hide_index=True, width="stretch")


def main():
    try:
        modelo, vectorizador = cargar_modelo()
    except Exception:
        st.error(
            "No fue posible cargar los artefactos del modelo. "
            "Verifique que los archivos .pkl estén en la carpeta de la aplicación."
        )
        st.stop()

    if "historial" not in st.session_state:
        st.session_state.historial = []

    st.title("🐾 Clasificador de Mensajes")
    st.caption("Clínica Veterinaria — Proyecto Capstone")
    st.write(
        "Escriba o pegue un mensaje del chat para estimar su categoría. "
        "La herramienta apoya la recepción y no sustituye la revisión profesional."
    )

    mensaje = st.text_area(
        "Mensaje del cliente:",
        height=100,
        max_chars=5000,
        placeholder="Ej.: Mi gato no ha comido en dos días y está muy decaído",
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        clasificar = st.button(
            "🔍 Clasificar mensaje", width="stretch", type="primary"
        )
    with col2:
        limpiar = st.button("🗑️ Limpiar historial", width="stretch")

    if limpiar:
        st.session_state.historial = []
        st.rerun()

    if clasificar:
        resultado = clasificar_mensaje(modelo, vectorizador, mensaje)
        mostrar_resultado(resultado)
        if resultado.estado != "entrada_invalida":
            guardar_en_historial(mensaje, resultado)

    if st.session_state.historial:
        st.divider()
        st.subheader("Historial de esta sesión")
        st.dataframe(
            pd.DataFrame(st.session_state.historial),
            hide_index=True,
            width="stretch",
        )

    st.caption(
        "Prototipo académico. No asigna prioridad clínica, no diagnostica y no genera "
        "recomendaciones de tratamiento. Las alertas deben ser validadas por la veterinaria."
    )


if __name__ == "__main__":
    main()
