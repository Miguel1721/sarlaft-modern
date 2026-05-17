"""
TEST DE SCRAPPERS - Pruebas unitarias
Autor: antigravity AI
"""

import asyncio
import sys
import os

# Agregar ruta al path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


async def test_runt():
    """Test RUNT scraper"""
    from scrapers.runt_scraper import RUNTScraper

    print("\n" + "="*60)
    print("TEST: RUNT SCRAPER")
    print("="*60)

    scraper = RUNTScraper()

    # NOTA: Usar placa real para pruebas
    placa_prueba = "ABC123"

    resultado = await scraper.consultar_vehiculo(placa_prueba)

    print("\n📋 RESULTADO:")
    import json
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    return resultado


async def test_ofac():
    """Test OFAC scraper"""
    from scrapers.ofac_scraper import OFACScraper

    print("\n" + "="*60)
    print("TEST: OFAC SCRAPER")
    print("="*60)

    scraper = OFACScraper()

    nombre_prueba = "JUAN PEREZ GARCIA"

    resultado = await scraper.consultar_persona(nombre_prueba)

    print("\n📋 RESULTADO:")
    import json
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    return resultado


async def test_fuzzy():
    """Test fuzzy matching"""
    from scrapers.fuzzy_matching import (
        buscar_coincidencia,
        normalizar_nombre,
        comparar_nombres
    )

    print("\n" + "="*60)
    print("TEST: FUZZY MATCHING")
    print("="*60)

    # Test normalización
    nombres = [
        "JUAN CARLOS PÉREZ GARCÍA",
        "MARÍA FERNANDA LÓPEZ",
        "CARLOS ALBERTO RODRÍGUEZ"
    ]

    print("\n1. NORMALIZACIÓN:")
    for nombre in nombres:
        normalizado = normalizar_nombre(nombre)
        print(f"  {nombre} → {normalizado}")

    # Test búsqueda
    print("\n2. BÚSQUEDA:")
    nombre_busqueda = "JUAN A PEREZ GARCIA"  # Similar al primero
    coincidencias = buscar_coincidencia(nombre_busqueda, nombres)

    for c in coincidencias:
        print(f"  ✓ {c['nombre_original']}: {c['score']}%")

    # Test comparación
    print("\n3. COMPARACIÓN:")
    nombre1 = "CARLOS ALBERTO PEREZ"
    nombre2 = "CARLOS A PEREZ"

    resultado = comparar_nombres(nombre1, nombre2)
    print(f"  {nombre1} vs {nombre2}")
    print(f"  Ratio: {resultado['ratio']}")
    print(f"  WRatio: {resultado['WRatio']}")
    print(f"  ¿Coincide? {resultado['coincidencia']}")

    return coincidencias


async def test_cache():
    """Test cache manager"""
    from scrapers.utils.cache_manager import CacheManager

    print("\n" + "="*60)
    print("TEST: CACHE MANAGER")
    print("="*60)

    cache = CacheManager(ttl_horas=1)

    # Guardar
    await cache.guardar("TEST", "clave1", {"datos": "valor1"})
    await cache.guardar("TEST", "clave2", {"datos": "valor2"})

    # Obtener
    dato1 = await cache.obtener("TEST", "clave1")
    print(f"\n  ✅ Cache HIT: {dato1}")

    # Estadísticas
    stats = await cache.obtener_estadisticas()
    print(f"\n  📊 Estadísticas: {stats}")

    return stats


async def main():
    """Ejecutar todos los tests"""

    print("\n" + "="*60)
    print("🧪 SUITE DE TESTS - SCRAPERS SARLAFT")
    print("="*60)

    tests = [
        ("Fuzzy Matching", test_fuzzy),
        ("Cache Manager", test_cache),
        ("OFAC Scraper", test_ofac),
        ("RUNT Scraper", test_runt),
        ("SIMIT Scraper", test_simit),
    ]

    resultados = {}

    for nombre, test_func in tests:
        try:
            print(f"\n\n▶️  EJECUTANDO: {nombre}")
            resultado = await test_func()
            resultados[nombre] = "✅ PASÓ"
        except Exception as e:
            print(f"❌ ERROR en {nombre}: {e}")
            resultados[nombre] = f"❌ FALLÓ: {e}"

    # Resumen
    print("\n\n" + "="*60)
    print("📊 RESUMEN DE TESTS")
    print("="*60)

    for nombre, estado in resultados.items():
        print(f"  {estado} - {nombre}")

    return resultados


async def test_simit():
    """Test SIMIT scraper"""
    from scrapers.simit_scraper import SIMITScraper

    print("\n" + "="*60)
    print("TEST: SIMIT SCRAPER")
    print("="*60)

    scraper = SIMITScraper()

    # Cédula de prueba
    cedula_prueba = "1022394742"

    resultado = await scraper.consultar_multas(cedula_prueba)

    print("\n📋 RESULTADO:")
    import json
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    return resultado


if __name__ == "__main__":
    asyncio.run(main())
