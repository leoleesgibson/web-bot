import asyncio
from bot.browser import BrowserManager
from bot.actions import random_scroll, click_first_link

async def run_bot():
    browser_manager = BrowserManager(headless=False)
    page = await browser_manager.start()

    await page.goto("https://example.com")
    await random_scroll(page)
    await click_first_link(page)

    await asyncio.sleep(5)
    await browser_manager.close()

if __name__ == "__main__":
    asyncio.run(run_bot())
