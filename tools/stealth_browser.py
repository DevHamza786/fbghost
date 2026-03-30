import asyncio
import random
import time
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from loguru import logger

class StealthBrowser:
    def __init__(self, user_data_dir="profiles/meta_profile"):
        self.user_data_dir = user_data_dir
        self.browser_context = None
        self.playwright = None

    async def start(self):
        self.playwright = await async_playwright().start()
        # Non-headless is better for "stealth" but harder on servers.
        # We'll default to visible for debugging or headless=False.
        self.browser_context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=False, # Meta is sensitive to headless
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
                "--window-size=1920,1080"
            ]
        )
        return self.browser_context

    async def stop(self):
        if self.browser_context:
            await self.browser_context.close()
        if self.playwright:
            await self.playwright.stop()

    async def new_stealth_page(self):
        page = await self.browser_context.new_page()
        await stealth_async(page)
        return page

    @staticmethod
    async def human_type(page, selector, text):
        """Types like a human with random delays and mistakes."""
        await page.wait_for_selector(selector)
        await page.click(selector)
        for char in text:
            await page.type(selector, char, delay=random.randint(100, 250))
            if random.random() < 0.05: # 5% chance of typo
                await asyncio.sleep(0.5)
                # backspace simulation? 
                pass 
        await asyncio.sleep(0.5)

    @staticmethod
    async def human_move_and_click(page, selector):
        """Moves mouse in a non-linear path to the element before clicking."""
        # Simple implementation: move to random points then target
        # A more advanced implementation would use Bézier curves.
        box = await page.locator(selector).bounding_box()
        if not box:
            return
        
        target_x = box['x'] + box['width'] / 2
        target_y = box['y'] + box['height'] / 2
        
        # Start from current position
        # For simplicity, move in few steps
        steps = 5
        for i in range(steps):
             offset_x = random.randint(-50, 50)
             offset_y = random.randint(-50, 50)
             await page.mouse.move(target_x + offset_x, target_y + offset_y)
             await asyncio.sleep(random.uniform(0.1, 0.3))
             
        await page.mouse.move(target_x, target_y)
        await asyncio.sleep(random.uniform(0.2, 0.5))
        await page.click(selector)

async def test_stealth():
    browser = StealthBrowser()
    ctx = await browser.start()
    page = await browser.new_stealth_page()
    await page.goto("https://www.google.com")
    logger.info(f"Page title: {await page.title()}")
    await browser.stop()

if __name__ == "__main__":
    asyncio.run(test_stealth())
