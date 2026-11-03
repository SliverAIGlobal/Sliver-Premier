import os
import io
import base64
import logging
from typing import List, Optional, Tuple
import numpy as np
import cv2
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from engine import ColoringPageEngine, MetadataGenerator
from gumroad_client import GumroadPublisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ColorWorldFastAPI")

app = FastAPI(
    title="2026 Color World - Instant Coloring Page Engine",
    description="Sub-50ms Image to Line-Art Conversion Engine with Stamped Copyright, Aspect Cropping, Detail Optimization, and Gumroad API Integration",
    version="1.2.0"
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
async def convert_image_endpoint(
    file: UploadFile = File(...),
    aspect_ratio: Optional[str] = Form("original"),
    detail_level: Optional[float] = Form(0.5),
    crop_x: Optional[int] = Form(None),
    crop_y: Optional[int] = Form(None),
    crop_w: Optional[int] = Form(None),
    crop_h: Optional[int] = Form(None),
    white_label_brand: Optional[str] = Form(None)
):
    """Uploads an image, applies optional cropping, aspect ratio, and detail optimization (<50ms), returning line art preview + AI metadata."""
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file format.")

        crop_box = None
        if all(v is not None for v in (crop_x, crop_y, crop_w, crop_h)):
            crop_box = (crop_x, crop_y, crop_w, crop_h)

        pil_img, elapsed_ms = engine.convert_image(
            image_input=img,
            crop_box=crop_box,
            aspect_ratio=aspect_ratio,
            detail_level=detail_level or 0.5,
            white_label_brand=white_label_brand
        )

        buffered = io.BytesIO()
        pil_img.save(buffered, format="PNG")
        base64_img = base64.b64encode(buffered.getvalue()).decode("utf-8")

        metadata = meta_gen.generate_metadata(
            filename=file.filename or "template",
            detail_level=detail_level or 0.5
        )

        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "conversion_ms": round(elapsed_ms, 2),
            "benchmark_passed": elapsed_ms < 50.0,
            "aspect_ratio": aspect_ratio,
            "detail_level": detail_level,
            "dimensions": f"{pil_img.size[0]}x{pil_img.size[1]}",
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

@app.post("/api/publish/bundle")
async def publish_bundle_endpoint():
    """Publishes the $49.99 Trending Ten Commercial Bundle to Gumroad."""
    res = publisher.publish_trending_bundle()
    return JSONResponse(res)

@app.post("/api/publish/corporate")
async def publish_corporate_endpoint():
    """Publishes the $5,000 Corporate White Label Lifetime Training License to Gumroad."""
    res = publisher.publish_corporate_license()
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
    """Serves the standalone single-page Web App UI from index.html."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/corporate", response_class=HTMLResponse)
async def get_corporate_dashboard():
    """Serves the corporate white label training sheet engine."""
    with open("corporate_white_label.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)
