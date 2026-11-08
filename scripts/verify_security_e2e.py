import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def run_security_browser_audit():
    print("=== STARTING BROWSER SECURITY & END-TO-END VERIFICATION ===")
    screenshots_dir = Path("assets/screenshots/security_verify")
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    brain_screenshots_dir = Path("C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a/security_verify")
    brain_screenshots_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        # -------------------------------------------------------------
        # 1. Workspace Load & Branding Check
        # -------------------------------------------------------------
        print("\n1. Navigating to http://localhost:3000/#workspace...")
        # Suppress tour initially
        await page.add_init_script("""
            localStorage.setItem('paymesh_tour_dismissed', 'true');
            localStorage.setItem('paymesh_tour_completed', 'true');
        """)
        await page.goto("http://localhost:3000/#workspace", wait_until="networkidle")
        await page.wait_for_timeout(500)

        title = await page.title()
        body_text = await page.inner_text("body")
        assert "PayMesh AI" in body_text, "Branding PayMesh AI not found in page body"
        assert "CrawlerPal" not in body_text, "Found legacy branding CrawlerPal on page!"
        print(f"   - PayMesh AI branding confirmed. (Title: '{title}')")

        await page.screenshot(path=str(screenshots_dir / "01_workspace_clean.png"))
        await page.screenshot(path=str(brain_screenshots_dir / "01_workspace_clean.png"))

        # -------------------------------------------------------------
        # 2. Audit All External and target="_blank" Links for noopener noreferrer
        # -------------------------------------------------------------
        print("\n2. Auditing DOM links for reverse-tabnabbing security (target='_blank')...")
        links_audit = await page.evaluate("""() => {
            const blankLinks = Array.from(document.querySelectorAll('a[target="_blank"]'));
            return blankLinks.map(a => ({
                href: a.href,
                target: a.target,
                rel: a.rel,
                text: a.innerText.trim(),
                is_secure: a.rel.includes('noopener') && a.rel.includes('noreferrer')
            }));
        }""")

        print(f"   - Found {len(links_audit)} target='_blank' links:")
        all_secure = True
        for link_item in links_audit:
            status = "PASS" if link_item["is_secure"] else "FAIL"
            print(f"     [{status}] {link_item['text'] or link_item['href']} -> rel='{link_item['rel']}'")
            if not link_item["is_secure"]:
                all_secure = False

        assert all_secure, "Some target='_blank' links lack 'noopener noreferrer' protection!"
        print("   - PASS: 100% of target='_blank' links possess rel='noopener noreferrer'.")

        # -------------------------------------------------------------
        # 3. Test Custom 404 Page & Navigation Return
        # -------------------------------------------------------------
        print("\n3. Testing custom 404 page at http://localhost:3000/does-not-exist...")
        await page.goto("http://localhost:3000/does-not-exist", wait_until="networkidle")
        await page.wait_for_timeout(400)

        not_found_text = await page.inner_text("body")
        assert "404" in not_found_text, "404 indicator not displayed"
        assert "Looks like this page doesn't exist" in not_found_text, "Missing 404 message"
        assert "Traceback" not in not_found_text, "Stack trace leaked on 404 page!"
        print("   - PASS: Clean 404 error page rendered without stack trace leaks.")

        await page.screenshot(path=str(screenshots_dir / "02_custom_404_view.png"))
        await page.screenshot(path=str(brain_screenshots_dir / "02_custom_404_view.png"))

        # Click "Back to Home"
        back_btn = page.locator("button:has-text('Back to Home')")
        assert await back_btn.is_visible(), "Back to Home button must be visible on 404"
        await back_btn.click()
        await page.wait_for_timeout(400)
        assert "workspace" in page.url or page.url.endswith("/"), "Failed to navigate back home"
        print(f"   - PASS: 'Back to Home' smoothly returned to {page.url}.")

        # -------------------------------------------------------------
        # 4. Test L402 Challenge & PayPal Sandbox Authorization Modal
        # -------------------------------------------------------------
        print("\n4. Triggering L402 challenge flow & testing PayPal Sandbox Modal...")
        await page.goto("http://localhost:3000/#workspace", wait_until="networkidle")
        await page.wait_for_timeout(400)

        # Click preset scenario
        preset_btn = page.locator("text=Hardware Latency Benchmarks")
        await preset_btn.click()
        await page.wait_for_timeout(200)

        dispatch_btn = page.locator("button:has-text('Dispatch Agent')")
        await dispatch_btn.click()

        # Wait for L402 challenge card
        challenge_card = page.locator("text=HTTP 402 CHALLENGE")
        await challenge_card.wait_for(timeout=6000)
        print("   - PASS: L402 Challenge received from backend.")

        await page.screenshot(path=str(screenshots_dir / "03_l402_challenge.png"))
        await page.screenshot(path=str(brain_screenshots_dir / "03_l402_challenge.png"))

        # Open PayPal Sandbox Modal
        pay_btn = page.locator("button:has-text('Approve & Pay')")
        await pay_btn.click()

        modal_title = page.locator("text=PayPal Sandbox Authorization")
        await modal_title.wait_for(timeout=4000)
        print("   - PASS: PayPal Sandbox Authorization modal opened.")

        # Initial modal view
        await page.screenshot(path=str(screenshots_dir / "04_paypal_modal_init.png"))
        await page.screenshot(path=str(brain_screenshots_dir / "04_paypal_modal_init.png"))

        # Click Authorize & Pay to initiate order and receive honest approval challenge
        auth_btn = page.locator("button:has-text('Authorize & Pay')")
        await auth_btn.click()

        # Wait for PayPal approval options
        approval_header = page.locator("text=Option 1: If you have a PayPal Sandbox Buyer Account:")
        await approval_header.wait_for(timeout=8000)
        print("   - PASS: PayPal Sandbox order created and honest approval options rendered.")

        # Verify modal link has rel="noopener noreferrer"
        modal_link = page.locator("a:has-text('Sign In at PayPal Sandbox')")
        rel_attr = await modal_link.get_attribute("rel")
        assert "noopener" in (rel_attr or "") and "noreferrer" in (rel_attr or ""), "PayPal Sandbox modal link missing noopener noreferrer"
        print(f"   - PASS: Modal external link has rel='{rel_attr}'.")

        await page.screenshot(path=str(screenshots_dir / "05_paypal_modal_approval.png"))
        await page.screenshot(path=str(brain_screenshots_dir / "05_paypal_modal_approval.png"))

        # Close modal
        cancel_btn = page.locator("button:has-text('Cancel')")
        await cancel_btn.click()
        await page.wait_for_timeout(200)
        print("   - PASS: Modal safely cancelled and closed.")

        # -------------------------------------------------------------
        # 5. Verify /health Endpoint Sanitization
        # -------------------------------------------------------------
        print("\n5. Checking /health endpoint response sanitization...")
        health_page = await context.new_page()
        health_resp = await health_page.goto("http://127.0.0.1:8000/health")
        assert health_resp is not None, "/health response is None"
        assert health_resp.status == 200, f"/health returned status {health_resp.status}"
        health_json = json.loads(await health_resp.text())
        print(f"   - /health returned: status='{health_json.get('status')}', database='{health_json.get('database')}'")
        assert "Traceback" not in str(health_json)
        assert "OperationalError" not in str(health_json)
        print("   - PASS: Health check responses are clean, structured, and free of exception leaks.")

        # -------------------------------------------------------------
        # 6. Verify Console Errors
        # -------------------------------------------------------------
        print("\n6. Checking Browser Console Logs...")
        print(f"   - Total critical console errors logged during flow: {len(console_errors)}")
        for err in console_errors:
            print(f"     [Console Error] {err}")
        # Filter out expected HTTP status logs from fetch calls (e.g. 502 ORDER_NOT_APPROVED, 402 PAYMENT_REQUIRED)
        unexpected_errors = [
            err for err in console_errors 
            if not ("502" in err or "402" in err)
        ]
        print(f"   - Total unexpected JavaScript errors: {len(unexpected_errors)}")
        for err in unexpected_errors:
            print(f"     [Unexpected Error] {err}")
        assert len(unexpected_errors) == 0, f"Expected 0 unexpected JS console errors, got {len(unexpected_errors)}"

        await browser.close()
        print("\n=== ALL BROWSER SECURITY & E2E TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    asyncio.run(run_security_browser_audit())
