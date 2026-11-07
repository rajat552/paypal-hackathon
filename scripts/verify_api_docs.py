from playwright.sync_api import sync_playwright

def verify_api_docs_click():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to http://localhost:3000...")
        page.goto("http://localhost:3000", wait_until="networkidle")

        # If tour is open on load, dismiss it via Exit Tour
        exit_tour_btn = page.locator('button:has-text("Exit Tour")')
        if exit_tour_btn.is_visible():
            print("Tour opened on URL visit as expected. Clicking 'Exit Tour' to test Navbar interaction...")
            exit_tour_btn.click()
            page.wait_for_timeout(500)

        # Find the API Docs button in Navbar
        api_docs_link = page.locator('a[href="/docs"]:has-text("API Docs")')
        assert api_docs_link.is_visible(), "API Docs link should be visible in navbar"
        print("Found API Docs link in Navbar.")

        # Click the link and wait for the new page / tab
        with context.expect_page() as new_page_info:
            api_docs_link.click()
        
        new_page = new_page_info.value
        new_page.wait_for_load_state("networkidle")
        print(f"New tab opened with URL: {new_page.url}")

        # Verify page title and Swagger UI content
        title = new_page.title()
        print(f"New tab title: '{title}'")
        assert "Swagger UI" in title or "PayMesh" in title, f"Expected Swagger UI in title, got: {title}"

        # Verify Swagger UI DOM elements exist
        swagger_ui = new_page.locator("#swagger-ui")
        assert swagger_ui.is_visible(), "Swagger UI container (#swagger-ui) should be visible on the new tab!"
        print("PASS: #swagger-ui container is visible on the new tab!")

        # Verify that Onboarding Tour is NOT rendered on the new tab
        tour_dialog = new_page.locator('[data-tour="tour-card"]')
        assert tour_dialog.count() == 0, "Tour dialog should NOT be rendered on Swagger UI!"
        print("PASS: Tour dialog is NOT present on the API docs tab.")

        # Take screenshot of the Swagger UI tab
        new_page.screenshot(path="assets/screenshots/api_docs_swagger_ui.png")
        print("Saved screenshot to assets/screenshots/api_docs_swagger_ui.png")

        browser.close()
        print("ALL API DOCS CHECKS PASSED!")

if __name__ == "__main__":
    verify_api_docs_click()
