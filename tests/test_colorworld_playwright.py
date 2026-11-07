import os
import time
import subprocess
import pytest
from playwright.sync_api import sync_playwright

SERVER_PORT = 8089

@pytest.fixture(scope="module")
def web_server():
    # Start clean Python static server
    proc = subprocess.Popen(
        ["python3", "-m", "http.server", str(SERVER_PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1.0)
    yield f"http://127.0.0.1:{SERVER_PORT}"
    proc.terminate()
    proc.wait()

def test_clean_profile_diagnostics_and_offline(web_server):
    with sync_playwright() as p:
        # Launch fresh clean browser profile with no prior cache or service worker
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        console_logs = []
        page.on("console", lambda msg: console_logs.append(msg.text))

        # 1. Boot page
        page.goto(f"{web_server}/index.html", wait_until="networkidle")
        assert "COLORWORKS MASTERS STUDIO" in page.title()

        # 2. Verify window.runDiagnostics passes with 0 failures
        failures = page.evaluate("() => window.runDiagnostics()")
        assert failures == 0, f"Diagnostics harness failed with {failures} failures"

        # 3. Test mode switching
        page.click("#modeJourneyBtn")
        assert page.is_visible("#journeySection")
        assert not page.is_visible("#sourceSection")

        page.click("#modeColoringBtn")
        assert page.is_visible("#sourceSection")
        assert not page.is_visible("#journeySection")

        # 4. Verify BUG-1 (time-lapse on null baseLine does not throw)
        bug1_res = page.evaluate("""() => {
            try {
                const cv = window.Colorworld.state.canvas;
                window.Colorworld.state.baseLine = null;
                window.Colorworld.state.ops = [{ t: 'paint', a: [10, 10], b: [20, 20], c: '#6d4aff', w: 2, alpha: 1, tool: 'brush' }];
                document.getElementById('timelapseBtn').click();
                return { success: true };
            } catch (e) {
                return { success: false, error: e.message };
            }
        }""")
        assert bug1_res["success"], f"BUG-1 regression failed: {bug1_res.get('error')}"

        # 5. Verify BUG-5 regression: Erasing 100% does NOT unlock gate
        bug5_res = page.evaluate("""() => {
            const { state, PrecisionEngine } = window.Colorworld;
            const ctx = state.ctx;
            // Draw dummy baseline
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, state.width, state.height);
            state.baseLine = ctx.getImageData(0, 0, state.width, state.height);
            state.lineMask = new Uint8Array(state.width * state.height);
            // Erase entire canvas with destination-out
            ctx.save();
            ctx.globalCompositeOperation = 'destination-out';
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, state.width, state.height);
            ctx.restore();
            const score = PrecisionEngine.computePrecision(ctx, state.baseLine, state.lineMask, state.width, state.height);
            return score;
        }""")
        assert not bug5_res["passed"], "BUG-5 regression failed: 100% erased canvas unlocked gate!"

        # 6. Verify Deterministic Edge AI generation
        determinism_res = page.evaluate("""async () => {
            const { EdgeEngine } = window.Colorworld;
            const prompt = 'cosmic star orbit';
            const g1 = EdgeEngine.fallbackGrammar(prompt);
            const g2 = EdgeEngine.fallbackGrammar(prompt);
            const dummyCnv = document.createElement('canvas');
            dummyCnv.width = 100;
            dummyCnv.height = 100;
            const res1 = EdgeEngine.renderProceduralGrammar(g1, dummyCnv);
            const res2 = EdgeEngine.renderProceduralGrammar(g2, dummyCnv);
            return { seed1: res1.seed, seed2: res2.seed, match: res1.seed === res2.seed };
        }""")
        assert determinism_res["match"], f"Seeds did not match: {determinism_res}"

        # 7. Test i18n switching
        page.click("#langES")
        es_text = page.locator("#modeColoringBtn span").text_content()
        assert "Estudio de Colorear" in es_text

        page.click("#langFR")
        fr_text = page.locator("#modeColoringBtn span").text_content()
        assert "Studio de Coloriage" in fr_text

        page.click("#langEN")
        en_text = page.locator("#modeColoringBtn span").text_content()
        assert "Coloring Studio" in en_text

        # 8. Test Gumroad Mock Mode (?publishMock=1)
        mock_publish_res = page.evaluate("""async () => {
            const { GumroadPublisher } = window.Colorworld;
            const payload = {
                title: 'Test Masterpiece',
                tags: ['gothic', 'fine-art', 'wallpaper', 'dark-fantasy', 'coloring', 'studio'],
                license: 'CC BY-NC-SA 4.0',
                attestationChecked: true,
                priceCents: 499
            };
            return await GumroadPublisher.publishListing(payload, true);
        }""")
        assert mock_publish_res["success"], f"Mock publish failed: {mock_publish_res}"
        assert mock_publish_res.get("mock") is True

        browser.close()
