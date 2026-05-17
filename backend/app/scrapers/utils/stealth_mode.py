"""
STEALTH MODE - Configuración anti-detección para Playwright
Autor: antigravity AI
"""

from playwright.async_api import async_playwright, Browser, BrowserContext


async def crear_navegador_stealth(headless: bool = True) -> tuple[Browser, BrowserContext]:
    """
    Crea navegador con configuración anti-detección

    Returns:
        (browser, context)
    """

    p = await async_playwright().start()

    browser = await p.chromium.launch(
        headless=headless,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--window-size=1920,1080',
            '--disable-infobars',
            '--disable-extensions',
            '--disable-gpu',
            '--start-maximized'
        ]
    )

    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        locale='es-CO',
        timezone_id='America/Bogota',
        permissions=['geolocation', 'notifications'],
        accept_downloads=False,
        java_script_enabled=True
    )

    # Inyectar scripts anti-detección
    await context.add_init_script("""
        // Ocultar propiedad webdriver
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });

        // Ocultar automatización
        Object.defineProperty(navigator, 'automation', {
            get: () => undefined
        });

        // Falsificar plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                {
                    0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
                    description: "Portable Document Format",
                    filename: "internal-pdf-viewer",
                    length: 1,
                    name: "Chrome PDF Plugin"
                }
            ]
        });

        // Falsificar languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['es-CO', 'es', 'en-US', 'en']
        });

        // Falsificar platform
        Object.defineProperty(navigator, 'platform', {
            get: () => 'Win32'
        });

        // Falsificar hardwareConcurrency
        Object.defineProperty(navigator, 'hardwareConcurrency', {
            get: () => 8
        });

        // Falsificar deviceMemory
        Object.defineProperty(navigator, 'deviceMemory', {
            get: () => 8
        });

        // Ocultar Playwright
        window.chrome = {
            runtime: {}
        };

        // Permisos de notificación
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
    """)

    return browser, context


async def esperar_segundos(segundos: float):
    """Espera N segundos (para simular comportamiento humano)"""
    import asyncio
    await asyncio.sleep(segundos)


async def escribir_como_humano(page, selector: str, texto: str, velocidad_ms: float = 100):
    """
    Escribe texto simulando comportamiento humano (con delays aleatorios)

    Args:
        page: Página de Playwright
        selector: Selector CSS del input
        texto: Texto a escribir
        velocidad_ms: Milisegundos promedio entre teclas
    """
    import random
    import asyncio

    await page.click(selector)
    await asyncio.sleep(random.uniform(0.3, 0.7))

    for char in texto:
        await page.keyboard.type(char)
        # Variación aleatoria: +/- 40% de la velocidad
        delay = velocidad_ms * random.uniform(0.6, 1.4) / 1000
        await asyncio.sleep(delay)


async def scroll_como_humano(page, cantidad_pixeles: int = None):
    """
    Hace scroll simulando comportamiento humano

    Args:
        page: Página de Playwright
        cantidad_pixeles: Cantidad de pixeles (aleatorio si es None)
    """
    import random
    import asyncio

    if cantidad_pixeles is None:
        cantidad_pixeles = random.randint(200, 500)

    await page.evaluate(f'window.scrollBy(0, {cantidad_pixeles})')
    await asyncio.sleep(random.uniform(0.5, 1.5))


async def mouse_movimiento_aleatorio(page):
    """Mueve el mouse aleatoriamente para parecer humano"""
    import random
    import asyncio

    width = 1920
    height = 1080

    for _ in range(random.randint(3, 7)):
        x = random.randint(100, width - 100)
        y = random.randint(100, height - 100)

        await page.mouse.move(x, y, steps=random.randint(10, 20))
        await asyncio.sleep(random.uniform(0.1, 0.3))
