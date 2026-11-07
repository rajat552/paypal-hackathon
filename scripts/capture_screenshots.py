import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

SCREENSHOT_DIR = Path("assets/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

async def capture_all():
    print("Launching Chromium for PayMesh AI UI capture...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 960})
        page = await context.new_page()

        # 1. Main Workspace
        print("Capturing 01: Agent Workspace...")
        await page.goto("http://localhost:8000", wait_until="networkidle")
        await asyncio.sleep(2)
        await page.screenshot(path=SCREENSHOT_DIR / "01-agent-workspace.png", full_page=False)

        # 2. Trigger Agent Run -> HTTP 402 Challenge
        print("Dispatching agent task to generate L402 Challenge...")
        run_btn = page.locator("button:has-text('Dispatch Agent')").first
        if await run_btn.is_visible():
            await run_btn.click()
            await page.wait_for_selector("text=HTTP 402 CHALLENGE", timeout=10000)
            await asyncio.sleep(1.5)
            await page.screenshot(path=SCREENSHOT_DIR / "02-l402-challenge.png", full_page=False)

            # 3. Open Modal -> Authorize & Pay -> Unlocked Intelligence
            print("Opening PayPal Sandbox Order modal & capturing...")
            pay_btn = page.locator("button:has-text('Approve & Pay via PayPal Sandbox')").first
            if await pay_btn.is_visible():
                await pay_btn.click()
                await asyncio.sleep(1)
                
                # Click modal Authorize & Pay
                auth_btn = page.locator("button:has-text('Authorize & Pay')").first
                if await auth_btn.is_visible():
                    await auth_btn.click()
                    await page.wait_for_selector("text=Unlocked:", timeout=15000)
                    await asyncio.sleep(2)
                    await page.screenshot(path=SCREENSHOT_DIR / "03-unlocked-intelligence.png", full_page=False)

        # 4. Spending Policy & Trust Engine Tab
        print("Capturing 04: Spending Policy Manager...")
        policy_tab = page.locator("button:has-text('Spending Policy & Trust')").first
        await policy_tab.click()
        await asyncio.sleep(1.5)
        await page.screenshot(path=SCREENSHOT_DIR / "04-spending-policy.png", full_page=False)

        # 5. API & Data Catalogue Tab
        print("Capturing 05: API & Data Catalogue...")
        catalogue_tab = page.locator("button:has-text('API & Data Catalogue')").first
        await catalogue_tab.click()
        await asyncio.sleep(1.5)
        await page.screenshot(path=SCREENSHOT_DIR / "05-marketplace-catalogue.png", full_page=False)

        # 6. Financial Ledger (AG Grid) Tab
        print("Capturing 06: AG Grid Financial Ledger...")
        analytics_tab = page.locator("button:has-text('Financial Ledger (AG Grid)')").first
        await analytics_tab.click()
        await asyncio.sleep(2)
        await page.screenshot(path=SCREENSHOT_DIR / "06-financial-ledger.png", full_page=False)

        # 7. Merchant Studio Tab
        print("Capturing 07: Merchant Studio...")
        merchant_tab = page.locator("button:has-text('Merchant Studio')").first
        await merchant_tab.click()
        await asyncio.sleep(1.5)
        await page.screenshot(path=SCREENSHOT_DIR / "07-merchant-studio.png", full_page=False)

        await browser.close()
        print("All screenshots successfully captured and saved in docs/assets/screenshots/!")

if __name__ == "__main__":
    asyncio.run(capture_all())
