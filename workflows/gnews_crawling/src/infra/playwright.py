from playwright.async_api import async_playwright, BrowserContext
import random

_PLAYWRIGHT = None
_BROWSER = None
_CONTEXTS = []


async def get_browser_context(max_num: int = 5) -> BrowserContext:
    global _PLAYWRIGHT, _BROWSER, _CONTEXTS

    if _PLAYWRIGHT is None:
        _PLAYWRIGHT = await async_playwright().start()

    if len(_CONTEXTS) <= max_num:
        _BROWSER = await _PLAYWRIGHT.chromium.launch(headless=True)
        _CONTEXTS.extend([await _BROWSER.new_context() for _ in range(max_num - len(_CONTEXTS))])

    return _CONTEXTS[random.randint(0, len(_CONTEXTS) - 1)]


async def shutdown_browser():
    global _PLAYWRIGHT, _BROWSER, _CONTEXTS

    for context in _CONTEXTS:
        await context.close()

    await _BROWSER.close()
    await _PLAYWRIGHT.stop()

    _PLAYWRIGHT = None
    _BROWSER = None
    _CONTEXTS = []