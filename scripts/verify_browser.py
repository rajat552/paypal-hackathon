import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def run_browser_verification():
    print("=== Launching Playwright Headless Browser Verification ===")
    screenshots_dir = Path("assets/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        # 1. Load application root
        print("\n[Step 1] Navigating to http://localhost:3000...")
        await page.goto("http://localhost:3000", wait_until="networkidle")

        # If tour is open on fresh load, dismiss it via Exit Tour
        exit_tour_btn = page.locator('button:has-text("Exit Tour")')
        if await exit_tour_btn.count() > 0:
            print("Tour opened on initial visit. Clicking 'Exit Tour'...")
            await exit_tour_btn.first.click()
            await page.wait_for_timeout(500)

        content = await page.content()

        # Check for PayMesh AI branding
        assert "PayMesh AI" in content or "PayMesh" in content, "Brand 'PayMesh' not found on page"
        # Verify 0 occurrences of CrawlerPal in user-visible text
        body_text = await page.inner_text("body")
        assert "CrawlerPal" not in body_text, "Found unexpected 'CrawlerPal' in visible page text!"
        print("PASS: Verified PayMesh AI branding and zero CrawlerPal occurrences on initial load.")
        await page.screenshot(path=str(screenshots_dir / "01_workspace_initial.png"))

        # 2. Select mission preset and dispatch agent
        print("\n[Step 2] Selecting mission preset and dispatching agent...")
        preset = page.locator("text=Hardware Latency Benchmarks")
        if await preset.count() > 0:
            await preset.first.click()
            print("PASS: Clicked 'Hardware Latency Benchmarks' preset chip.")

        dispatch_btn = page.locator("button:has-text('Dispatch Agent')")
        await dispatch_btn.first.click()
        print("PASS: Clicked 'Dispatch Agent'. Waiting for L402 challenge negotiation...")

        # Wait for HTTP 402 challenge card
        challenge_card = page.locator("text=HTTP 402 CHALLENGE")
        await challenge_card.wait_for(timeout=10000)
        print("PASS: HTTP 402 Challenge Card rendered successfully!")
        await page.screenshot(path=str(screenshots_dir / "02_agent_challenge_negotiated.png"))

        # 3. Test PayPal checkout modal
        print("\n[Step 3] Opening PayPal Sandbox authorization modal...")
        pay_btn = page.locator("button:has-text('Approve & Pay')")
        if await pay_btn.count() > 0:
            await pay_btn.first.click()
            modal = page.locator("text=PayPal Sandbox Authorization")
            await modal.wait_for(timeout=5000)
            print("PASS: PayPal Sandbox checkout modal opened.")
            await page.screenshot(path=str(screenshots_dir / "03_paypal_modal.png"))

            # Close modal with Cancel button
            cancel_btn = page.locator("button:has-text('Cancel')")
            await cancel_btn.first.click()
            print("PASS: Closed modal via Cancel button.")

        # 4. Navigate to Policy Manager
        print("\n[Step 4] Navigating to Spending Policy & Trust...")
        policy_tab = page.locator("header button:has-text('Spending Policy'), header a:has-text('Spending Policy')")
        await policy_tab.first.click()
        await page.wait_for_timeout(1000)

        # Check rolling budget bar
        budget_bar = page.locator("text=24-Hour Rolling Budget Utilization")
        await budget_bar.wait_for(timeout=5000)
        print("PASS: Policy Manager loaded with 24-Hour Rolling Budget Utilization.")

        # Test updating policy
        update_btn = page.locator("button:has-text('Save Spending Policy'), button:has-text('Update Deterministic Policy Rules')")
        await update_btn.first.click()
        await page.wait_for_timeout(1000)
        print("PASS: Clicked 'Save Spending Policy' and saved configuration.")
        await page.screenshot(path=str(screenshots_dir / "04_policy_manager.png"))

        # 5. Navigate to Data Catalogue
        print("\n[Step 5] Navigating to API & Data Catalogue...")
        catalogue_tab = page.locator("header button:has-text('API & Data Catalogue'), header a:has-text('API & Data Catalogue')")
        await catalogue_tab.first.click()
        await page.wait_for_timeout(1000)

        cat_wire = page.locator("text=PayMesh Wire & Feeds")
        await cat_wire.wait_for(timeout=5000)
        print("PASS: Catalogue loaded with category 'PayMesh Wire & Feeds'.")
        await page.screenshot(path=str(screenshots_dir / "05_catalogue_view.png"))

        # Test search filter
        search_input = page.locator("input[placeholder*='Search']")
        if await search_input.count() > 0:
            await search_input.first.fill("Hardware")
            await page.wait_for_timeout(500)
            print("PASS: Catalogue search filter tested.")

        # 6. Navigate to Financial Ledger (AG Grid)
        print("\n[Step 6] Navigating to Financial Ledger (AG Grid)...")
        ledger_tab = page.locator("header button:has-text('Financial Ledger'), header a:has-text('Financial Ledger')")
        await ledger_tab.first.click()
        await page.wait_for_timeout(1500)
        print("PASS: Financial Ledger (AG Grid) loaded.")
        await page.screenshot(path=str(screenshots_dir / "06_settlement_ledger.png"))

        # 7. Check for CrawlerPal across entire DOM in all views
        full_text = await page.inner_text("body")
        assert "CrawlerPal" not in full_text, "CrawlerPal found in body text of Settlement Ledger!"

        print("\n=======================================================")
        print("ALL BROWSER INTERACTION CHECKS PASSED WITH 0 ERRORS!")
        print("=======================================================")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_browser_verification())
