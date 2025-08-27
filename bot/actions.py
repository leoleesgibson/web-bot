import asyncio
import random

async def random_scroll(page, steps=5):
    for _ in range(steps):
        scroll_amount = random.randint(200, 800)
        await page.mouse.wheel(0, scroll_amount)
        await asyncio.sleep(random.uniform(1, 3))

async def click_first_link(page):
    links = await page.query_selector_all("a")
    if links:
        await links[0].click()
        await asyncio.sleep(2)
