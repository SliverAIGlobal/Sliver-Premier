import os
import io
import base64
import logging
import numpy as np
import cv2
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from engine import ColoringPageEngine, MetadataGenerator
from gumroad_client import GumroadPublisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ColorWorldFastAPI")

app = FastAPI(
    title="2026 Color World - Instant Coloring Page Engine",
    description="Sub-50ms Image to Line-Art Conversion Engine with Stamped Copyright and Gumroad API Integration",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = ColoringPageEngine(copyright_text="© 2026 Color World")
meta_gen = MetadataGenerator()
publisher = GumroadPublisher()

class PublishRequest(BaseModel):
    name: str
    price_cents: int = 399
    tags: List[str]
    promo_code: str = "SUBSCRIBE50"

class LicenseVerifyRequest(BaseModel):
    product_id: str
    license_key: str
    increment_uses_count: bool = True

class LicenseActionRequest(BaseModel):
    product_id: str
    license_key: str

@app.post("/api/convert")
async def convert_image_endpoint(file: UploadFile = File(...)):
    """Uploads an image, converts to line art in <50ms with stamp, and returns base64 preview + AI metadata."""
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file format.")

        # Sub-50ms conversion
        pil_img, elapsed_ms = engine.convert_image(img)

        # Encode PIL image to Base64 PNG
        buffered = io.BytesIO()
        pil_img.save(buffered, format="PNG")
        base64_img = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Metadata generation
        metadata = meta_gen.generate_metadata(file.filename or "template")

        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "conversion_ms": round(elapsed_ms, 2),
            "benchmark_passed": elapsed_ms < 50.0,
            "copyright_stamp": "© 2026 Color World",
            "image_data_url": f"data:image/png;base64,{base64_img}",
            "metadata": metadata
        })

    except Exception as e:
        logger.exception("Conversion failed")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/publish")
async def publish_endpoint(req: PublishRequest):
    """Publishes page to Gumroad for $3.99 with license keys and 50% promo code."""
    res = publisher.publish_product(
        name=req.name,
        price_cents=req.price_cents,
        tags=req.tags,
        promo_code=req.promo_code
    )
    return JSONResponse(res)

@app.post("/api/license/verify")
async def verify_license_endpoint(req: LicenseVerifyRequest):
    """Verifies a Gumroad customer license key."""
    res = publisher.verify_license(req.product_id, req.license_key, req.increment_uses_count)
    return JSONResponse(res)

@app.post("/api/license/enable")
async def enable_license_endpoint(req: LicenseActionRequest):
    """Enables a Gumroad customer license."""
    res = publisher.enable_license(req.product_id, req.license_key)
    return JSONResponse(res)

@app.post("/api/license/disable")
async def disable_license_endpoint(req: LicenseActionRequest):
    """Disables a Gumroad customer license."""
    res = publisher.disable_license(req.product_id, req.license_key)
    return JSONResponse(res)

@app.get("/api/earnings")
async def get_earnings_endpoint(year: int = Query(2025)):
    """Retrieves tax center annual earnings summary from Gumroad."""
    res = publisher.get_earnings(year)
    return JSONResponse(res)

@app.get("/api/payouts")
async def get_payouts_endpoint():
    """Retrieves upcoming and completed payouts from Gumroad."""
    res = publisher.get_payouts()
    return JSONResponse(res)

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serves the interactive single-page Web App UI for image upload, live preview, and Gumroad publishing."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026 Color World - Instant Coloring Page Engine</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .card { background-color: #1e293b; border: 1px solid #334155; border-radius: 12px; }
        .btn-accent { background: linear-gradient(135deg, #6366f1, #a855f7); color: white; font-weight: 600; border: none; }
        .btn-accent:hover { background: linear-gradient(135deg, #4f46e5, #9333ea); color: white; }
        .badge-ms { font-size: 1.1rem; background-color: #10b981; color: #022c22; font-weight: bold; }
        .tag-badge { background-color: #334155; color: #38bdf8; margin-right: 6px; margin-bottom: 6px; display: inline-block; padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; }
        .preview-img { max-height: 480px; object-fit: contain; border-radius: 8px; border: 2px dashed #475569; }
    </style>
</head>
<body class="py-5">
    <div class="container">
        <div class="text-center mb-5">
            <h1 class="display-4 fw-bold" style="background: linear-gradient(90deg, #38bdf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">2026 Color World Engine</h1>
            <p class="lead text-slate-400">Sub-50ms Instant Image-to-Coloring Page Converter & Gumroad Listing Engine</p>
        </div>

        <div class="row g-4">
            <!-- Left: Upload & Controls -->
            <div class="col-lg-5">
                <div class="card p-4 shadow-lg">
                    <h4 class="card-title text-light mb-3">Upload Image</h4>
                    <div class="mb-3">
                        <input class="form-control bg-dark text-light border-secondary" type="file" id="imageInput" accept="image/*">
                    </div>
                    <button class="btn btn-accent w-100 py-2 fs-5" id="convertBtn" onclick="processImage()">Convert Instant (&lt; 50ms)</button>

                    <div id="statusAlert" class="mt-3 alert d-none"></div>

                    <div id="metadataBox" class="mt-4 d-none">
                        <hr class="border-secondary">
                        <h5 class="text-info mb-2">AI Indexing Metadata</h5>
                        <div class="mb-2">
                            <label class="text-secondary small">Template Name:</label>
                            <input type="text" id="metaName" class="form-control bg-dark text-light border-secondary form-control-sm">
                        </div>
                        <div class="mb-2">
                            <label class="text-secondary small">Title:</label>
                            <input type="text" id="metaTitle" class="form-control bg-dark text-light border-secondary form-control-sm">
                        </div>
                        <div class="mb-3">
                            <label class="text-secondary small">6 Filter Tags:</label>
                            <div id="tagsContainer" class="mt-1"></div>
                        </div>
                        <button class="btn btn-success w-100 py-2 font-monospace" onclick="publishGumroad()">Publish to Gumroad ($3.99)</button>
                    </div>
                </div>
            </div>

            <!-- Right: Preview Screen -->
            <div class="col-lg-7">
                <div class="card p-4 shadow-lg text-center h-100">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="card-title text-light m-0">Coloring Page Preview</h4>
                        <span id="speedBadge" class="badge badge-ms d-none">0.00 ms</span>
                    </div>
                    <div class="d-flex align-items-center justify-content-center bg-dark rounded p-3" style="min-height: 400px;">
                        <img id="resultPreview" src="" class="img-fluid preview-img d-none" alt="Coloring Page Result">
                        <div id="placeholderText" class="text-muted fs-5">Upload an image to see sub-50ms line art conversion with stamped copyright</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentMetadata = null;

        async function processImage() {
            const input = document.getElementById('imageInput');
            if (!input.files[0]) {
                alert('Please select an image file first.');
                return;
            }

            const formData = new FormData();
            formData.append('file', input.files[0]);

            const convertBtn = document.getElementById('convertBtn');
            convertBtn.disabled = true;
            convertBtn.innerText = 'Converting...';

            try {
                const res = await fetch('/api/convert', { method: 'POST', body: formData });
                const data = await res.json();

                if (data.success) {
                    document.getElementById('resultPreview').src = data.image_data_url;
                    document.getElementById('resultPreview').classList.remove('d-none');
                    document.getElementById('placeholderText').classList.add('d-none');

                    const badge = document.getElementById('speedBadge');
                    badge.innerText = `${data.conversion_ms} ms (${data.benchmark_passed ? '< 50ms PASSED' : 'SLOW'})`;
                    badge.classList.remove('d-none');

                    currentMetadata = data.metadata;
                    document.getElementById('metaName').value = data.metadata.name;
                    document.getElementById('metaTitle').value = data.metadata.title;

                    const tagsDiv = document.getElementById('tagsContainer');
                    tagsDiv.innerHTML = data.metadata.tags.map(t => `<span class="tag-badge">#${t}</span>`).join('');
                    document.getElementById('metadataBox').classList.remove('d-none');
                }
            } catch (e) {
                alert('Conversion failed: ' + e);
            } finally {
                convertBtn.disabled = false;
                convertBtn.innerText = 'Convert Instant (< 50ms)';
            }
        }

        async function publishGumroad() {
            if (!currentMetadata) return;

            const name = document.getElementById('metaName').value;
            const tags = currentMetadata.tags;

            const res = await fetch('/api/publish', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: name, price_cents: 399, tags: tags, promo_code: 'SUBSCRIBE50' })
            });

            const data = await res.json();
            const statusDiv = document.getElementById('statusAlert');
            statusDiv.classList.remove('d-none', 'alert-danger', 'alert-success');

            if (data.success) {
                statusDiv.classList.add('alert-success');
                statusDiv.innerHTML = `<strong>Success!</strong> Published in ${data.mode.toUpperCase()} mode.<br>URL: <a href="${data.product_url}" target="_blank" class="text-decoration-underline text-light">${data.product_url}</a><br>Promo Code: <strong>${data.promo_code}</strong> (${data.discount})`;
            } else {
                statusDiv.classList.add('alert-danger');
                statusDiv.innerText = 'Gumroad API Error: ' + data.error;
            }
        }
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)
