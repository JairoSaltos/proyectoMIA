"""Controles de seguridad alrededor del clasificador Cat Clinic.

Este módulo no modifica ni reentrena el modelo. Valida la entrada, ejecuta la
predicción original y decide cuándo debe intervenir una persona.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Any


MIN_SCORE_REVISION = 0.35

# Estas categorías contienen información clínica y, por diseño, requieren
# supervisión humana. La aplicación no asigna prioridad médica.
CATEGORIAS_CLINICAS = {
    "medicamentos_recetas",
    "resultados_examenes",
    "seguimiento_clinico",
    "triaje_clinico",
}

# Lista conservadora para detectar mensajes que no deben quedar únicamente en
# manos del clasificador. Debe ser revisada y aprobada por la veterinaria.
PATRONES_SENSIBLES = {
    "sangrado": r"\b(?:sangr\w*|hemorrag\w*)\b",
    "convulsión": r"\bconvulsion\w*\b",
    "dificultad respiratoria": r"\b(?:no\s+(?:puede\s+)?respir\w*|dificultad\w*\s+(?:para\s+)?respir\w*)\b",
    "accidente": r"\b(?:atropell\w*|accidente\w*)\b",
    "posible intoxicación": r"\b(?:intoxic\w*|envenen\w*)\b",
    "pérdida de conciencia": r"\b(?:inconsciente\w*|desmay\w*)\b",
    "dificultad para orinar": r"\b(?:no\s+(?:puede\s+)?orin\w*|sin\s+orin\w*)\b",
    "solicitud urgente": r"\b(?:emergencia\w*|urgente\w*)\b",
}


@dataclass(frozen=True)
class ResultadoClasificacion:
    estado: str
    mensaje_usuario: str | None = None
    texto_limpio: str = ""
    categoria: str | None = None
    score: float | None = None
    scores_por_categoria: dict[str, float] | None = None
    requiere_revision: bool = False
    motivos_revision: tuple[str, ...] = ()


def limpiar_texto(texto: Any) -> str:
    """Replica la limpieza usada por la versión original de la aplicación."""
    if texto is None:
        return ""
    texto_limpio = str(texto).lower()
    texto_limpio = re.sub(r"http\S+|www\S+", "", texto_limpio)
    texto_limpio = re.sub(r"[^a-záéíóúñü\s]", " ", texto_limpio)
    texto_limpio = re.sub(r"\s+", " ", texto_limpio).strip()
    return texto_limpio


def _sin_tildes(texto: str) -> str:
    normalizado = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in normalizado if not unicodedata.combining(c))


def detectar_terminos_sensibles(texto_limpio: str) -> tuple[str, ...]:
    texto_normalizado = _sin_tildes(texto_limpio)
    return tuple(
        etiqueta
        for etiqueta, patron in PATRONES_SENSIBLES.items()
        if re.search(patron, texto_normalizado, flags=re.IGNORECASE)
    )


def evaluar_revision(
    categoria: str,
    score: float | None,
    texto_limpio: str,
) -> tuple[bool, tuple[str, ...]]:
    motivos: list[str] = []

    if score is None:
        motivos.append("el modelo no proporciona un score estimado")
    elif score < MIN_SCORE_REVISION:
        motivos.append(f"score estimado menor a {MIN_SCORE_REVISION:.0%}")

    if categoria in CATEGORIAS_CLINICAS:
        motivos.append("contenido clasificado en una categoría clínica")

    terminos = detectar_terminos_sensibles(texto_limpio)
    if terminos:
        motivos.append("términos sensibles: " + ", ".join(terminos))

    return bool(motivos), tuple(motivos)


def clasificar_mensaje(modelo: Any, vectorizador: Any, mensaje: Any) -> ResultadoClasificacion:
    """Clasifica solo entradas válidas y agrega controles de revisión humana."""
    texto_limpio = limpiar_texto(mensaje)

    if not texto_limpio:
        return ResultadoClasificacion(
            estado="entrada_invalida",
            mensaje_usuario="Ingrese un mensaje con texto antes de clasificar.",
        )

    vector = vectorizador.transform([texto_limpio])
    if vector.nnz == 0:
        return ResultadoClasificacion(
            estado="informacion_insuficiente",
            mensaje_usuario=(
                "El mensaje no contiene términos reconocidos por el modelo. "
                "Solicite más contexto y realice una revisión humana."
            ),
            texto_limpio=texto_limpio,
            requiere_revision=True,
            motivos_revision=("ningún término reconocido por el vectorizador",),
        )

    categoria = str(modelo.predict(vector)[0])
    score: float | None = None
    scores_por_categoria: dict[str, float] | None = None

    if hasattr(modelo, "predict_proba"):
        probabilidades = modelo.predict_proba(vector)[0]
        clases = [str(clase) for clase in modelo.classes_]
        scores_por_categoria = {
            clase: float(probabilidad)
            for clase, probabilidad in zip(clases, probabilidades)
        }
        score = max(scores_por_categoria.values())

    requiere_revision, motivos = evaluar_revision(categoria, score, texto_limpio)

    return ResultadoClasificacion(
        estado="clasificado",
        texto_limpio=texto_limpio,
        categoria=categoria,
        score=score,
        scores_por_categoria=scores_por_categoria,
        requiere_revision=requiere_revision,
        motivos_revision=motivos,
    )
