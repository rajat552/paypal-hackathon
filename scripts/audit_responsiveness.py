import asyncio
import os
from playwright.async_api import async_playwright

VIEWPORTS = [
    {"name": "01_small_mobile_320x568", "width": 320, "height": 568},
    {"name": "02_standard_mobile_375x667", "width": 375, "height": 667},
    {"name": "03_large_mobile_390x844", "width": 390, "height": 844},
    {"name": "04_modern_mobile_430x932", "width": 430, "height": 932},
    {"name": "05_small_tablet_768x1024", "width": 768, "height": 1024},
    {"name": "06_large_tablet_1024x768", "width": 1024, "height": 768},
    {"name": "07_small_laptop_1280x720", "width": 1280, "height": 720},
    {"name": "08_standard_laptop_1366x768", "width": 1366, "height": 768},
    {"name": "09_desktop_1440x900", "width": 1440, "height": 900},
    {"name": "10_large_desktop_1920x1080", "width": 1920, "height": 1080},
]

TABS = [
    {"id": "workspace", "hash": "#workspace", "name": "Agent Workspace"},
    {"id": "policy", "hash": "#policy", "name": "Spending Policy"},
    {"id": "catalogue", "hash": "#catalogue", "name": "API Catalogue"},
    {"id": "analytics", "hash": "#analytics", "name": "Financial Ledger"},
    {"id": "publisher", "hash": "#publisher", "name": "Merchant Studio"},
]

async def audit_responsiveness():
    print("=== STARTING COMPLETE RESPONSIVENESS AUDIT ===")
    os.makedirs("assets/screenshots/responsive_audit", exist_ok=True)
    os.makedirs("C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a/responsive", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Suppress tour initially so we test page layouts cleanly
        await page.add_init_script("""
            localStorage.setItem('paymesh_tour_dismissed', 'true');
            localStorage.setItem('paymesh_tour_completed', 'true');
        """)

        overflow_issues = []

        for vp in VIEWPORTS:
            print(f"\n--- Testing Viewport: {vp['name']} ({vp['width']}x{vp['height']}) ---")
            await page.set_viewport_size({"width": vp["width"], "height": vp["height"]})

            for tab in TABS:
                url = f"http://localhost:3000/{tab['hash']}"
                await page.goto(url, wait_until="networkidle")
                await page.wait_for_timeout(400)

                # Check horizontal overflow
                metrics = await page.evaluate("""() => {
                    const docEl = document.documentElement;
                    const body = document.body;
                    const scrollWidth = Math.max(docEl.scrollWidth, body.scrollWidth);
                    const clientWidth = docEl.clientWidth;
                    const hasHorizontalOverflow = scrollWidth > clientWidth + 1;
                    return { scrollWidth, clientWidth, hasHorizontalOverflow };
                }""")

                if metrics["hasHorizontalOverflow"]:
                    issue = f"Viewport {vp['name']} on Tab {tab['id']}: scrollWidth ({metrics['scrollWidth']}px) > clientWidth ({metrics['clientWidth']}px)"
                    print(f"  [OVERFLOW DETECTED] {issue}")
                    overflow_issues.append(issue)
                else:
                    print(f"  [OK] {tab['name']} width: {metrics['clientWidth']}px, scroll: {metrics['scrollWidth']}px")

                # Capture key screenshot on small mobile, modern mobile, tablet, and desktop
                if vp["width"] in [320, 390, 768, 1280, 1920]:
                    shot_path = f"assets/screenshots/responsive_audit/{vp['width']}px_{tab['id']}.png"
                    await page.screenshot(path=shot_path)
                    await page.screenshot(path=f"C:/Users/LENOVO/.gemini/antigravity/brain/4216dfba-b02d-40c3-a0cd-9c315d6b113a/responsive/{vp['width']}px_{tab['id']}.png")

        print("\n=== AUDIT SUMMARY ===")
        if overflow_issues:
            print(f"Detected {len(overflow_issues)} horizontal overflow issues:")
            for iss in overflow_issues:
                print(f" - {iss}")
        else:
            print("No horizontal page-level overflow detected across tested viewports!")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(audit_responsiveness())

