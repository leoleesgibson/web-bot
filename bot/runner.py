import asyncio
from bot.browser import BrowserManager
from bot.actions import random_scroll, search_and_navigate, browse_like_human

async def run_bot():
    browser_manager = BrowserManager(headless=False)
    page = await browser_manager.start()

    search_query = "FrontPageAfrica"
    target_url = "frontpageafricaonline.com"

    # Search and navigate to the target website
    await search_and_navigate(page, search_query, target_url)
    
    # Browse the website like a human for 5 minutes
    await browse_like_human(page, session_duration_minutes=5)

    # Final pause before closing
    await asyncio.sleep(10)
    await browser_manager.close()

if __name__ == "__main__":
    asyncio.run(run_bot())
