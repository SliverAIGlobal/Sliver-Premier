import asyncio
import os
import http.server
import socketserver
import threading
from playwright.async_api import async_playwright

PORT = 8089

def start_server():
    os.chdir('/app')
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    httpd.serve_forever()

async def run_e2e():
    # Start server in thread
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    await asyncio.sleep(1)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        print(f"Navigating to http://localhost:{PORT}/index.html...")
        await page.goto(f"http://localhost:{PORT}/index.html")
        await page.wait_for_selector("h1")

        title = await page.text_content("h1")
        print("Page Header:", title)
        assert "Atemporal Reweaver" in title

        # Verify WASM Garden SVG rendering
        svg = await page.wait_for_selector('[data-testid="lumina-garden-svg"]')
        assert svg is not None
        circles = await page.query_selector_all('[data-testid="lumina-garden-svg"] circle')
        print(f"Rendered SVG leaves count: {len(circles)}")
        assert len(circles) >= 12

        # Verify Initial TokeX and Mastery
        tokex_text = await page.text_content('[data-testid="tokex-balance"]')
        print("Initial TokeX:", tokex_text)
        assert "15" in tokex_text

        # Test Seed prompt click & sending message
        await page.click('[data-testid="seed-btn-0"]')
        print("Clicked emotion seed prompt")

        # Wait for Eva's response
        print("Waiting for Eva response in chat history...")
        await page.wait_for_selector('text=Eva • Atemporal Reweaver', timeout=10000)
        await asyncio.sleep(2) # Allow offline simulation delay

        chat_text = await page.text_content('[data-testid="chat-history-container"]')
        assert "Lumina Weaver" in chat_text
        print("Chat transcript contains User and Eva responses.")

        # Test Config Panel
        await page.click('[data-testid="config-toggle-btn"]')
        config_panel = await page.wait_for_selector('[data-testid="config-panel"]')
        assert config_panel is not None
        print("Config panel opened successfully.")

        # Close config panel
        await page.click('[data-testid="save-api-key-btn"]')
        await asyncio.sleep(0.5)

        # Take screenshot for visual verification
        screenshot_path = "/app/tests/e2e_verification.png"
        await page.screenshot(path=screenshot_path)
        print(f"Captured screenshot at {screenshot_path}")

        await browser.close()
        print("Playwright E2E verification test finished successfully! 🚀")

if __name__ == '__main__':
    asyncio.run(run_e2e())
