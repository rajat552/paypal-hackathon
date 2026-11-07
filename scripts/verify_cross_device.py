import asyncio
import os
from playwright.async_api import async_playwright

async def verify_cross_device():
    print("=== STARTING CROSS-DEVICE INTERACTION & REGRESSION TESTING ===")
    os.makedirs("assets/screenshots/responsive_verify", exist_ok=True)
    os.makedirs("C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a/responsive_verify", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # -------------------------------------------------------------
        # TEST 1: Small Mobile (320x568) - Mobile Navigation & Interactions
        # -------------------------------------------------------------
        print("\n1. Testing Mobile Hamburger Menu & Navigation on 320x568 (iPhone SE)...")
        context_mobile = await browser.new_context(viewport={"width": 320, "height": 568})
        page = await context_mobile.new_page()

        await page.add_init_script("""
            localStorage.setItem('paymesh_tour_dismissed', 'true');
            localStorage.setItem('paymesh_tour_completed', 'true');
        """)

        await page.goto("http://localhost:3000/#workspace", wait_until="networkidle")
        await page.wait_for_timeout(400)

        # Ensure hamburger button is visible
        menu_btn = page.locator("button[aria-label='Toggle Navigation Menu']")
        assert await menu_btn.is_visible(), "Hamburger button should be visible on 320px"
        
        # Click hamburger menu
        await menu_btn.click()
        await page.wait_for_timeout(300)
        
        # Verify drawer contains all tabs
        has_policy_link = await page.locator("div.lg\\:hidden button:has-text('Spending Policy & Trust')").is_visible()
        has_ledger_link = await page.locator("div.lg\\:hidden button:has-text('Financial Ledger')").is_visible()
        print(f"   - Mobile drawer opened: Policy link={has_policy_link}, Ledger link={has_ledger_link}")
        assert has_policy_link and has_ledger_link, "Mobile drawer must display navigation links"

        # Capture mobile menu open screenshot
        await page.screenshot(path="assets/screenshots/responsive_verify/01_mobile_320_menu_open.png")
        await page.screenshot(path="C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a/responsive_verify/01_mobile_320_menu_open.png")

        # Navigate to Spending Policy via mobile drawer
        await page.locator("div.lg\\:hidden button:has-text('Spending Policy & Trust')").click()
        await page.wait_for_timeout(400)
        assert "policy" in page.url, "URL should update to policy"
        has_policy_header = await page.locator("text=Autonomous Spending Guardrails & Policy").is_visible()
        print(f"   - Successfully navigated to Policy via mobile menu: {has_policy_header}")
        assert has_policy_header, "Policy page must render"

        # -------------------------------------------------------------
        # TEST 2: Modern Mobile (390x844) - Interactive Forms & Catalogue Search
        # -------------------------------------------------------------
        print("\n2. Testing Modern Mobile (390x844 - iPhone 13/14/15)...")
        await page.set_viewport_size({"width": 390, "height": 844})
        await page.goto("http://localhost:3000/#catalogue", wait_until="networkidle")
        await page.wait_for_timeout(400)

        # Search for Channel3
        search_input = page.locator("input[placeholder*='Search datasets']")
        await search_input.fill("Channel3")
        await page.wait_for_timeout(300)
        card_visible = await page.locator("h3:has-text('Channel3')").first.is_visible()
        print(f"   - Catalogue search filtered card on mobile: {card_visible}")
        assert card_visible, "Catalogue search must work responsively"

        await page.screenshot(path="assets/screenshots/responsive_verify/02_mobile_390_catalogue.png")
        await page.screenshot(path="C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a/responsive_verify/02_mobile_390_catalogue.png")

        # -------------------------------------------------------------
        # TEST 3: Financial Ledger & AG Grid on Tablet (768x1024)
        # -------------------------------------------------------------
        print("\n3. Testing Small Tablet (768x1024 - iPad Portrait)...")
        await page.set_viewport_size({"width": 768, "height": 1024})
        await page.goto("http://localhost:3000/#analytics", wait_until="networkidle")
        await page.wait_for_timeout(500)

        has_grid = await page.locator("div.ag-theme-alpine-dark").is_visible()
        print(f"   - AG Grid rendered cleanly on tablet: {has_grid}")
        assert has_grid, "AG Grid must render on tablet"

        await page.screenshot(path="assets/screenshots/responsive_verify/03_tablet_768_ledger.png")
        await page.screenshot(path="C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a/responsive_verify/03_tablet_768_ledger.png")

        # -------------------------------------------------------------
        # TEST 4: Large Tablet (1024x768 - iPad Landscape) - Compact Nav
        # -------------------------------------------------------------
        print("\n4. Testing Large Tablet (1024x768 - iPad Landscape)...")
        await page.set_viewport_size({"width": 1024, "height": 768})
        await page.goto("http://localhost:3000/#workspace", wait_until="networkidle")
        await page.wait_for_timeout(400)

        # Check compact nav tabs are visible
        has_nav = await page.locator("nav[data-tour='nav-tabs']").is_visible()
        print(f"   - Desktop compact nav visible on 1024px: {has_nav}")
        assert has_nav, "Compact nav must be visible on 1024px without overflow"

        # Verify scrollWidth <= clientWidth
        metrics = await page.evaluate("() => ({ scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth })")
        print(f"   - 1024px scrollWidth={metrics['scrollWidth']}px, clientWidth={metrics['clientWidth']}px")
        assert metrics['scrollWidth'] <= metrics['clientWidth'], "No overflow on 1024px"

        await page.screenshot(path="assets/screenshots/responsive_verify/04_tablet_1024_workspace.png")
        await page.screenshot(path="C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a/responsive_verify/04_tablet_1024_workspace.png")

        # -------------------------------------------------------------
        # TEST 5: Full Desktop (1440x900) - Merchant Studio & Preview
        # -------------------------------------------------------------
        print("\n5. Testing Desktop (1440x900)...")
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.goto("http://localhost:3000/#publisher", wait_until="networkidle")
        await page.wait_for_timeout(400)

        has_form = await page.locator("form").is_visible()
        has_preview = await page.locator("text=Catalogue Preview").is_visible()
        print(f"   - Publisher form visible: {has_form}, Preview visible: {has_preview}")
        assert has_form and has_preview, "Desktop publisher and preview must render side-by-side"

        await page.screenshot(path="assets/screenshots/responsive_verify/05_desktop_1440_publisher.png")
        await page.screenshot(path="C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a/responsive_verify/05_desktop_1440_publisher.png")

        # -------------------------------------------------------------
        # TEST 6: Checkout Modal Responsive Fit on 320x568
        # -------------------------------------------------------------
        print("\n6. Testing PayPal Sandbox Authorization Modal on 320x568 mobile...")
        await page.set_viewport_size({"width": 320, "height": 568})
        await page.goto("http://localhost:3000/#workspace", wait_until="networkidle")
        
        # Trigger L402 challenge negotiation by clicking sample preset scenario
        await page.locator("text=Hardware Latency Benchmarks").click()
        await page.wait_for_timeout(300)
        await page.locator("button:has-text('Dispatch Agent')").click()
        
        # Wait for L402 challenge card
        await page.wait_for_selector("text=HTTP 402 CHALLENGE", timeout=8000)
        print("   - L402 Challenge Card received on mobile")
        
        # Click "Approve & Pay with PayPal Sandbox" to open modal
        await page.locator("button:has-text('Approve & Pay')").click()
        await page.wait_for_selector("text=PayPal Sandbox Authorization", timeout=4000)
        print("   - PayPal Sandbox Authorization Modal opened on 320x568")

        # Verify modal fits screen
        modal_rect = await page.evaluate("""() => {
            const modal = document.querySelector('.animate-neo-pop');
            if (!modal) return null;
            const r = modal.getBoundingClientRect();
            return {
                width: r.width,
                height: r.height,
                right: r.right,
                bottom: r.bottom,
                windowWidth: window.innerWidth,
                windowHeight: window.innerHeight
            };
        }""")
        print(f"   - Modal dimensions on 320x568: width={modal_rect['width']}px, right={modal_rect['right']}px (screen width {modal_rect['windowWidth']}px)")
        assert modal_rect["right"] <= modal_rect["windowWidth"] + 1, "Modal must not exceed mobile screen width"

        await page.screenshot(path="assets/screenshots/responsive_verify/06_mobile_320_checkout_modal.png")
        await page.screenshot(path="C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a/responsive_verify/06_mobile_320_checkout_modal.png")

        # Close modal
        await page.locator("button:has-text('Cancel')").click()
        await page.wait_for_timeout(300)

        await browser.close()
        print("\n=== ALL CROSS-DEVICE INTERACTION TESTS PASSED! ===")

if __name__ == "__main__":
    asyncio.run(verify_cross_device())
