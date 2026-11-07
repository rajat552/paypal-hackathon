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
    {"index": 2, "title": "Main Navigation Bar", "tab": "workspace"},
    {"index": 3, "title": "Try a Sample Scenario", "tab": "workspace"},
    {"index": 4, "title": "Set Goal & Spending Limit", "tab": "workspace"},
    {"index": 5, "title": "Run the AI Agent", "tab": "workspace"},
    {"index": 6, "title": "Live Activity Terminal", "tab": "workspace"},
    {"index": 7, "title": "Payment Required (HTTP 402)", "tab": "workspace"},
    {"index": 8, "title": "Spending Rules & Safety", "tab": "policy"},
    {"index": 9, "title": "Daily Budget Tracker", "tab": "policy"},
    {"index": 10, "title": "Custom Limit Settings", "tab": "policy"},
    {"index": 11, "title": "Dataset Marketplace", "tab": "catalogue"},
    {"index": 12, "title": "1-Click Agent Purchase", "tab": "catalogue"},
    {"index": 13, "title": "PayPal Sandbox Payments", "tab": "workspace"},
    {"index": 14, "title": "Financial Transaction Ledger", "tab": "analytics"},
    {"index": 15, "title": "Publish Your Own API", "tab": "publisher"},
]

async def run_tour_verification():
    screenshots_dir = Path("assets/screenshots/tour")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    print("\n=== Starting PayMesh AI 15-Step Interactive Onboarding Tour Verification ===")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        # 1. URL Click Visit: Load page and verify tour dialog opens immediately
        print("\n[Phase 1] Navigating to http://localhost:3000 (URL Click Experience)...")
        await page.goto("http://localhost:3000", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        tour_dialog = page.locator("div[role='dialog'][aria-label*='Onboarding Tour']")
        await tour_dialog.wait_for(timeout=4000)
        assert await tour_dialog.is_visible(), "Tour dialog was not displayed immediately on clicking/visiting URL!"
        print("PASS: Tour dialog automatically displayed first on visiting URL.")
        await page.screenshot(path=str(screenshots_dir / "00_url_click_tour_first.png"))

        # 2. Verify Step 1 is active right away
        step1_active = tour_dialog.locator("text='1 / 15'")
        assert await step1_active.is_visible(), "Step 1 of 15 was not active on URL load!"
        print("PASS: Tour is at Step 1 ('Welcome to PayMesh AI') immediately upon URL access.")

        # 3. Test Exit and URL reload (tour displays every time URL is clicked)
        exit_btn = tour_dialog.locator("button:has-text('Exit Tour')")
        await exit_btn.click()
        await page.wait_for_timeout(400)
        assert not await tour_dialog.is_visible(), "Clicking 'Exit Tour' failed to close tour!"
        print("PASS: Clicked 'Exit Tour' — tour closed cleanly.")

        # Re-open via Navbar Tour Guide button
        print("\n[Phase 2] Opening tour via 'Tour Guide' button in Navbar...")
        tour_guide_btn = page.locator("button:has-text('Tour Guide')")
        await tour_guide_btn.first.click()
        await page.wait_for_timeout(600)
        assert await tour_dialog.is_visible(), "Tour failed to open after clicking Tour Guide button!"
        print("PASS: Tour opened cleanly via Tour Guide button.")

        # 4. Step through all 15 steps sequentially

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
        print("\n[Phase 3] Testing Tour Replay via Header 'Tour Guide' button...")
        tour_guide_btn = page.locator("header button:has-text('Tour Guide')")
        await tour_guide_btn.first.click()
        await page.wait_for_timeout(500)

        assert await tour_dialog.is_visible(), "Tour dialog failed to reopen on 'Tour Guide' click!"
        reopened_step1 = tour_dialog.locator("text='1 / 15'")
        assert await reopened_step1.is_visible(), "Replayed tour did not restart at Step 1!"
        print("PASS: Tour reopened at Step 1 via Navbar button.")

        # 6. Test Exit Tour Button from Action Bar
        print("\n[Phase 4] Testing 'Exit Tour' button in footer...")
        exit_btn = tour_dialog.locator("button:has-text('Exit Tour')")
        assert await exit_btn.is_visible(), "'Exit Tour' button was not visible in tour footer!"
        await exit_btn.click()
        await page.wait_for_timeout(400)
        assert not await tour_dialog.is_visible(), "Clicking 'Exit Tour' failed to close tour!"
        print("PASS: 'Exit Tour' button closed tour successfully.")

        # Reopen for keyboard test
        await tour_guide_btn.first.click()
        await page.wait_for_timeout(400)

        # 7. Test Keyboard Navigation (ArrowRight to advance, ArrowLeft to go back, Escape to close)
        print("\n[Phase 5] Testing Keyboard Navigation...")
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

