"""
FUZZY MATCHING - Coincidencia aproximada de nombres
Autor: antigravity AI
"""

import unicodedata
import re
from typing import List, Dict, Tuple
from rapidfuzz import fuzz, process


def normalizar_nombre(nombre: str) -> str:
    """Normaliza nombre para comparación"""
    if not nombre:
        return ""

    # Eliminar acentos
    nombre = unicodedata.normalize('NFKD', nombre)
    nombre = ''.join([c for c in nombre if not unicodedata.combining(c)])

    # Convertir a mayúsculas
    nombre = nombre.upper()

    # Eliminar caracteres especiales
    nombre = re.sub(r'[^A-Z\s]', '', nombre)

    # Eliminar espacios extra
    nombre = ' '.join(nombre.split())

    # Eliminar palabras comunes (stopwords)
    stopwords = ['DE', 'LA', 'EL', 'LOS', 'LAS', 'DEL', 'Y', 'EN', 'MI', 'POR']
    partes = nombre.split()
    filtradas = [p for p in partes if p not in stopwords]
    nombre = ' '.join(filtradas)

    return nombre.strip()


def buscar_coincidencia(
    nombre_busqueda: str,
    lista_nombres: List[str],
    umbral: int = 85,
    limite_resultados: int = 10
) -> List[Dict]:
    """
    Busca coincidencias usando fuzzy matching

    Args:
        nombre_busqueda: Nombre a buscar
        lista_nombres: Lista de nombres para buscar
        umbral: Score mínimo (0-100) para considerar coincidencia
        limite_resultados: Máximo número de resultados

    Returns:
        Lista de coincidencias con {nombre, score, match_normalizado}
    """

    if not nombre_busqueda or not lista_nombres:
        return []

    # Normalizar nombre de búsqueda
    nombre_normalizado = normalizar_nombre(nombre_busqueda)

    # Normalizar lista de nombres
    lista_normalizada = [normalizar_nombre(n) for n in lista_nombres]

    # Búsqueda con WRatio (Weighted Ratio) - mejor para nombres
    resultados = process.extract(
        nombre_normalizado,
        lista_normalizada,
        scorer=fuzz.WRatio,
        limit=limite_resultados
    )

    # Filtrar por umbral
    coincidencias = []
    for resultado, score, idx in resultados:
        if score >= umbral:
            coincidencias.append({
                "nombre_original": lista_nombres[idx],
                "nombre_normalizado": resultado,
                "score": score,
                "indice": idx
            })

    return coincidencias


def buscar_coincidancia_parcial(
    nombre_busqueda: str,
    lista_nombres: List[str],
    umbral: int = 80
) -> List[Dict]:
    """
    Busca coincidencia parcial (busca cada palabra por separado)

    Útil cuando el nombre puede estar en diferente orden
    """

    if not nombre_busqueda or not lista_nombres:
        return []

    # Dividir nombre en palabras
    nombre_normalizado = normalizar_nombre(nombre_busqueda)
    palabras_busqueda = nombre_normalizado.split()

    coincidencias = []

    for idx, nombre in enumerate(lista_nombres):
        nombre_norm = normalizar_nombre(nombre)
        palabras_nombre = nombre_norm.split()

        # Calcular score parcial
        scores = []
        for palabra_busqueda in palabras_busqueda:
            # Buscar mejor coincidencia para esta palabra
            parcial = process.extractOne(
                palabra_busqueda,
                palabras_nombre,
                scorer=fuzz.ratio
            )

            if parcial and parcial[1] >= umbral:
                scores.append(parcial[1])

        # Promedio de scores
        if scores:
            promedio = sum(scores) / len(scores)
            if promedio >= umbral:
                coincidencias.append({
                    "nombre_original": nombre,
                    "score": promedio,
                    "indice": idx,
                    "tipo": "PARCIAL"
                })

    # Ordenar por score descendente
    coincidencias.sort(key=lambda x: x["score"], reverse=True)

    return coincidencias


def comparar_nombres(nombre1: str, nombre2: str) -> Dict:
    """
    Compara dos nombres y retorna métricas de similitud

    Returns:
        Dict con diferentes métricas de comparación
    """

    norm1 = normalizar_nombre(nombre1)
    norm2 = normalizar_nombre(nombre2)

    return {
        "nombre1_normalizado": norm1,
        "nombre2_normalizado": norm2,
        "ratio": fuzz.ratio(norm1, norm2),
        "partial_ratio": fuzz.partial_ratio(norm1, norm2),
        "token_sort_ratio": fuzz.token_sort_ratio(norm1, norm2),
        "token_set_ratio": fuzz.token_set_ratio(norm1, norm2),
        "WRatio": fuzz.WRatio(norm1, norm2),
        "coincidencia": fuzz.WRatio(norm1, norm2) >= 85
    }


def limpiar_duplicados_lista(nombres: List[str], umbral: int = 90) -> List[str]:
    """
    Elimina duplicados de una lista usando fuzzy matching

    Args:
        nombres: Lista de nombres (puede tener duplicados)
        umbral: Score para considerar duplicados

    Returns:
        Lista sin duplicados
    """

    if not nombres:
        return []

    # Normalizar todos
    nombres_norm = [normalizar_nombre(n) for n in nombres]

    # Buscar duplicados
    unicos = []
    duplicados = set()

    for i, nombre in enumerate(nombres):
        if i in duplicados:
            continue

        unicos.append(nombre)

        # Buscar similares
        for j in range(i + 1, len(nombres)):
            if j in duplicados:
                continue

            score = fuzz.WRatio(nombres_norm[i], nombres_norm[j])
            if score >= umbral:
                duplicados.add(j)

    return unicos
