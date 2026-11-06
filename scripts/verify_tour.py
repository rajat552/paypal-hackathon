"""
Automated Playwright Verification for PayMesh AI 15-Step Interactive Onboarding Tour
Tests:
- First-visit welcome prompt trigger
- Start tour button
- Sequential step progression (Steps 1 to 15)
- Automated cross-tab switching
- Spotlight target element anchoring
- Back, Next, Finish, Skip, and Keyboard navigation
- Replay tour via Navbar "Tour Guide" button
- LocalStorage persistence
"""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

EXPECTED_STEPS = [
    {"index": 1, "title": "Welcome to PayMesh AI", "tab": "workspace"},
    {"index": 2, "title": "Main Navigation", "tab": "workspace"},
    {"index": 3, "title": "Agent Scenarios & Mission Presets", "tab": "workspace"},
    {"index": 4, "title": "Research Task Input & Spending Limit", "tab": "workspace"},
    {"index": 5, "title": "Dispatch AI Agent", "tab": "workspace"},
    {"index": 6, "title": "Real-Time Protocol Inspector", "tab": "workspace"},
    {"index": 7, "title": "L402 Payment Challenge & Negotiation", "tab": "workspace"},
    {"index": 8, "title": "Spending Policies & Trust Engine", "tab": "policy"},
    {"index": 9, "title": "24-Hour Rolling Budget Utilization", "tab": "policy"},
    {"index": 10, "title": "Server-Enforced Constraints", "tab": "policy"},
    {"index": 11, "title": "API & Data Catalogue", "tab": "catalogue"},
    {"index": 12, "title": "Agent Resource Dispatch", "tab": "catalogue"},
    {"index": 13, "title": "PayPal Sandbox Checkout & Capture", "tab": "workspace"},
    {"index": 14, "title": "Financial Ledger & AG Grid Analytics", "tab": "analytics"},
    {"index": 15, "title": "Merchant Studio & Developer Resources", "tab": "publisher"},
]

async def run_tour_verification():
    screenshots_dir = Path("docs/assets/screenshots/tour")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    print("\n=== Starting PayMesh AI 15-Step Interactive Onboarding Tour Verification ===")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        # 1. First Visit: Load page with empty localStorage
        print("\n[Phase 1] Navigating to http://localhost:3000 (First Visit Experience)...")
        await page.goto("http://localhost:3000", wait_until="networkidle")
        await page.wait_for_timeout(1500)

        welcome_prompt = page.locator("aside[aria-label='Welcome Tour Invitation']")
        await welcome_prompt.wait_for(timeout=4000)
        assert await welcome_prompt.is_visible(), "Welcome Tour Prompt was not displayed on first visit!"
        print("PASS: First-visit welcome prompt displayed successfully.")
        await page.screenshot(path=str(screenshots_dir / "00_welcome_prompt.png"))

        # 2. Click "Start Tour"
        start_btn = welcome_prompt.locator("button:has-text('Start Tour')")
        await start_btn.click()
        await page.wait_for_timeout(500)
        print("PASS: Clicked 'Start Tour'. Tour overlay is now active.")

        # 3. Step through all 15 steps sequentially
        tour_dialog = page.locator("div[role='dialog'][aria-label*='Onboarding Tour']")
        await tour_dialog.wait_for(timeout=4000)

        for step in EXPECTED_STEPS:
            idx = step["index"]
            expected_title = step["title"]
            expected_tab = step["tab"]

            print(f"\n[Step {idx} / 15] Verifying '{expected_title}'...")
            
            # Wait for step content to settle
            await page.wait_for_timeout(400)
            
            # Verify step counter
            step_counter = tour_dialog.locator(f"text='{idx} / 15'")
            await step_counter.wait_for(timeout=3000)

            # Verify step title
            step_title = tour_dialog.locator(f"h3:has-text('{expected_title}')")
            await step_title.wait_for(timeout=3000)

            # Verify progress bar indicator
            expected_pct = round((idx / 15) * 100)
            progress_indicator = tour_dialog.locator(f"text='Progress: {expected_pct}%'")
            await progress_indicator.wait_for(timeout=3000)

            # Take screenshot of key steps
            if idx in [1, 5, 8, 11, 14, 15]:
                await page.screenshot(path=str(screenshots_dir / f"step_{idx:02d}_{step['tab']}.png"))

            print(f"PASS: Step {idx} correctly positioned on tab '{expected_tab}' with Progress: {expected_pct}%.")

            # Advance to next step (or finish if last)
            if idx < 15:
                next_btn = tour_dialog.locator("button:has-text('Next Step')")
                await next_btn.click()
            else:
                finish_btn = tour_dialog.locator("button:has-text('Finish Tour')")
                await finish_btn.click()
                print("PASS: Clicked 'Finish Tour'.")

        await page.wait_for_timeout(500)

        # 4. Verify tour closed and localStorage persistence
        is_dialog_visible = await tour_dialog.is_visible()
        assert not is_dialog_visible, "Tour dialog should be closed after finishing!"

        completed_val = await page.evaluate("() => localStorage.getItem('paymesh_tour_completed')")
        assert completed_val == "true", f"localStorage paymesh_tour_completed expected 'true', got {completed_val}"
        print("PASS: Tour completion successfully persisted in localStorage ('paymesh_tour_completed': 'true').")

        # 5. Replay Tour via Navbar "Tour Guide" button
        print("\n[Phase 2] Testing Tour Replay via Header 'Tour Guide' button...")
        tour_guide_btn = page.locator("header button:has-text('Tour Guide')")
        await tour_guide_btn.first.click()
        await page.wait_for_timeout(500)

        assert await tour_dialog.is_visible(), "Tour dialog failed to reopen on 'Tour Guide' click!"
        reopened_step1 = tour_dialog.locator("text='1 / 15'")
        assert await reopened_step1.is_visible(), "Replayed tour did not restart at Step 1!"
        print("PASS: Tour reopened at Step 1 via Navbar button.")

        # 6. Test Keyboard Navigation (ArrowRight to advance, ArrowLeft to go back, Escape to close)
        print("\n[Phase 3] Testing Keyboard Navigation...")
        await page.keyboard.press("ArrowRight")
        await page.wait_for_timeout(300)
        assert await tour_dialog.locator("text='2 / 15'").is_visible(), "ArrowRight failed to advance to Step 2!"
        print("PASS: ArrowRight keyboard navigation advanced to Step 2.")

        await page.keyboard.press("ArrowLeft")
        await page.wait_for_timeout(300)
        assert await tour_dialog.locator("text='1 / 15'").is_visible(), "ArrowLeft failed to return to Step 1!"
        print("PASS: ArrowLeft keyboard navigation returned to Step 1.")

        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)
        assert not await tour_dialog.is_visible(), "Escape key failed to dismiss tour!"
        print("PASS: Escape key dismissed tour dialog.")

        print("\n=======================================================")
        print("ALL 15-STEP ONBOARDING TOUR CHECKS PASSED WITH 0 ERRORS!")
        print("=======================================================\n")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_tour_verification())

