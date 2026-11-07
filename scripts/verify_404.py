import asyncio
import os
from playwright.async_api import async_playwright

async def verify_404_experience():
    print("--- Starting PayMesh AI 404 Experience Verification ---")
    os.makedirs("assets/screenshots/404", exist_ok=True)
    os.makedirs("C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        # Suppress onboarding tour for clean test assertions
        await page.add_init_script("""
            localStorage.setItem('paymesh_tour_dismissed', 'true');
            localStorage.setItem('paymesh_tour_completed', 'true');
        """)

        # TEST 1: Direct navigation to invalid route /does-not-exist
        print("1. Navigating directly to invalid URL: http://localhost:3000/does-not-exist")
        await page.goto("http://localhost:3000/does-not-exist", wait_until="networkidle")
        await page.wait_for_selector("text=HTTP 404 — ROUTE UNRESOLVED", timeout=8000)
        
        # Verify 404 text content
        has_404 = await page.locator("h1:has-text('404')").is_visible()
        has_title = await page.locator("text=Looks like this page doesn't exist.").is_visible()
        has_desc = await page.locator("text=The page you're looking for may have been moved, renamed, or is temporarily unavailable.").is_visible()
        has_back_home = await page.locator("button:has-text('Back to Home')").is_visible()
        has_go_back = await page.locator("button:has-text('Go Back')").is_visible()
        has_diag = await page.locator("text=GET /does-not-exist").is_visible()
        
        print(f"   - 404 number visible: {has_404}")
        print(f"   - Main heading visible: {has_title}")
        print(f"   - SaaS description visible: {has_desc}")
        print(f"   - Diagnostic URL visible: {has_diag}")
        print(f"   - 'Back to Home' button: {has_back_home}")
        print(f"   - 'Go Back' button: {has_go_back}")
        assert has_404 and has_title and has_desc and has_back_home and has_go_back, "Missing required 404 UI elements"

        # Capture Desktop screenshot
        desktop_shot = "assets/screenshots/404/01_404_desktop.png"
        await page.screenshot(path=desktop_shot)
        await page.screenshot(path="C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a/404_desktop.png")
        print("   - Saved Desktop screenshot")

        # TEST 2: Tablet Resolution (768x1024)
        print("2. Testing Tablet Resolution (768x1024)...")
        await page.set_viewport_size({"width": 768, "height": 1024})
        await page.wait_for_timeout(500)
        await page.screenshot(path="assets/screenshots/404/02_404_tablet.png")
        await page.screenshot(path="C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a/404_tablet.png")
        print("   - Saved Tablet screenshot")

        # TEST 3: Mobile Resolution (375x667)
        print("3. Testing Mobile Resolution (375x667)...")
        await page.set_viewport_size({"width": 375, "height": 667})
        await page.wait_for_timeout(500)
        await page.screenshot(path="assets/screenshots/404/03_404_mobile.png")
        await page.screenshot(path="C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a/404_mobile.png")
        print("   - Saved Mobile screenshot")

        # Restore Desktop
        await page.set_viewport_size({"width": 1280, "height": 800})

        # TEST 4: Browser Refresh on 404 page
        print("4. Testing page refresh on 404 page...")
        await page.reload(wait_until="networkidle")
        await page.wait_for_selector("text=HTTP 404 — ROUTE UNRESOLVED", timeout=5000)
        print("   - Successfully preserved 404 page across browser reload")

        # TEST 5: Button 'Back to Home'
        print("5. Testing 'Back to Home' CTA click...")
        await page.click("button:has-text('Back to Home')")
        await page.wait_for_timeout(500)
        # Check workspace is visible and URL is updated
        current_url = page.url
        print(f"   - Current URL after Back to Home: {current_url}")
        has_workspace = await page.locator("h2:has-text('AI Commerce Agent')").first.is_visible()
        print(f"   - Workspace visible: {has_workspace}")
        assert "/#workspace" in current_url or current_url.endswith("/"), "URL should be reset to home"

        # TEST 6: Testing 'Go Back'
        print("6. Testing 'Go Back' CTA...")
        # First navigate to valid tab: Spending Policy
        await page.goto("http://localhost:3000/#policy", wait_until="networkidle")
        await page.wait_for_selector("text=Autonomous Spending Guardrails & Policy", timeout=5000)
        print("   - Visited /#policy")
        
        # Now navigate to invalid path
        await page.goto("http://localhost:3000/unknown-subroute", wait_until="networkidle")
        await page.wait_for_selector("text=HTTP 404 — ROUTE UNRESOLVED", timeout=5000)
        print("   - Hit 404 on /unknown-subroute")

        # Click Go Back
        await page.click("button:has-text('Go Back')")
        await page.wait_for_timeout(800)
        back_url = page.url
        print(f"   - URL after 'Go Back': {back_url}")
        assert "policy" in back_url or "workspace" in back_url, "Go Back should return to previous valid page"

        # TEST 7: Invalid hash route
        print("7. Testing invalid hash route: http://localhost:3000/#unrecognized-tab")
        await page.goto("http://localhost:3000/#unrecognized-tab", wait_until="networkidle")
        await page.wait_for_selector("text=HTTP 404 — ROUTE UNRESOLVED", timeout=5000)
        print("   - Invalid hash correctly displays 404 page")

        # TEST 8: Quick Jump Link from 404
        print("8. Testing quick jump link: 'Merchant Studio' from 404 page...")
        await page.locator("button:has-text('Merchant Studio')").last.click()
        await page.wait_for_timeout(600)
        has_publisher = await page.locator("text=Publish Dataset or API").first.is_visible()
        print(f"   - Merchant Studio active after quick jump: {has_publisher}")
        assert has_publisher, "Quick navigation should open Merchant Studio"

        await browser.close()
        print("--- ALL 404 VERIFICATION TESTS PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    asyncio.run(verify_404_experience())
