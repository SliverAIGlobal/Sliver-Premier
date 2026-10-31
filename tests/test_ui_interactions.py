import asyncio
import os
import http.server
import socketserver
import threading
from playwright.async_api import async_playwright

PORT = 8091

def start_server():
    os.chdir('/app')
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    httpd.serve_forever()

async def run_feature_test():
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    await asyncio.sleep(1)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(f"http://localhost:{PORT}/index.html")
        await page.wait_for_selector('[data-testid="feature-card-1"]')

        # Verify initial TokeX is 15
        tokex_el = await page.query_selector('[data-testid="tokex-balance"]')
        text = await tokex_el.text_content()
        assert "15" in text

        # Send a message to advance mastery to at least Level 1
        await page.click('[data-testid="seed-btn-0"]')
        await asyncio.sleep(2)

        # Check sample button or unlock button on tier 1
        sample_btn = await page.query_selector('[data-testid="sample-btn-1"]')
        if sample_btn:
            await sample_btn.click()
            await asyncio.sleep(0.5)
            status_el = await page.query_selector('[data-testid="status-1"]')
            assert status_el is not None
            status_text = await status_el.text_content()
            assert "Sampled" in status_text or "Rewoven" in status_text
            print("Feature Card Unlock/Sample Verified! Status:", status_text)

        await browser.close()
        print("UI Interactions test passed!")

if __name__ == '__main__':
    asyncio.run(run_feature_test())
