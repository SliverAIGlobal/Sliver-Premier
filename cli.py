import os
import sys
import json
import time
import argparse
import logging
import cv2
from engine import ColoringPageEngine, MetadataGenerator
from gumroad_client import GumroadPublisher

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ColorWorldCLI")

def process_batch(
    input_dir: str,
    output_dir: str,
    aspect_ratio: str = "original",
    detail_level: float = 0.5,
    publish_gumroad: bool = False
):
    if not os.path.exists(input_dir):
        logger.error(f"Input directory '{input_dir}' does not exist.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    engine = ColoringPageEngine(copyright_text="© 2026 Color World")
    meta_gen = MetadataGenerator()
    publisher = GumroadPublisher() if publish_gumroad else None

    valid_exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    image_files = [f for f in sorted(os.listdir(input_dir)) if os.path.splitext(f)[1].lower() in valid_exts]

    if not image_files:
        logger.warning(f"No valid image files found in '{input_dir}'.")
        return

    manifest = []
    logger.info(f"Starting batch conversion of {len(image_files)} image(s) [Aspect: {aspect_ratio}, Detail: {detail_level}]...")

    for idx, img_name in enumerate(image_files, 1):
        input_path = os.path.join(input_dir, img_name)
        img = cv2.imread(input_path)

        if img is None:
            logger.error(f"Skipping unreadable file: {img_name}")
            continue

        # 1. Image Conversion (<50ms benchmark with aspect ratio & detail level optimizer)
        out_img, elapsed_ms = engine.convert_image(
            image_input=img,
            aspect_ratio=aspect_ratio,
            detail_level=detail_level
        )

        # Save output image
        out_filename = f"coloring_{os.path.splitext(img_name)[0]}.png"
        out_path = os.path.join(output_dir, out_filename)
        out_img.save(out_path, format="PNG")

        # 2. Metadata Generation (exact 6 tags)
        metadata = meta_gen.generate_metadata(img_name, detail_level=detail_level)

        item_record = {
            "source_file": img_name,
            "converted_file": out_filename,
            "dimensions": f"{out_img.size[0]}x{out_img.size[1]}",
            "aspect_ratio": aspect_ratio,
            "detail_level": detail_level,
            "conversion_ms": round(elapsed_ms, 2),
            "metadata": metadata,
            "gumroad_listing": None
        }

        # 3. Optional Gumroad Publishing with file attachment and duplicate prevention
        if publish_gumroad and publisher is not None:
            listing = publisher.publish_product(
                name=metadata["name"],
                price_cents=399,
                tags=metadata["tags"],
                image_asset=out_path,
                prevent_duplicates=True
            )
            item_record["gumroad_listing"] = listing

        manifest.append(item_record)
        logger.info(f"[{idx}/{len(image_files)}] Processed {img_name} -> {out_filename} ({elapsed_ms:.2f} ms)")

    manifest_path = os.path.join(output_dir, "batch_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    logger.info(f"Batch processing completed successfully. Manifest saved to '{manifest_path}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="2026 Color World Batch Image Converter")
    parser.add_argument("--input", "-i", required=True, help="Input directory containing raw images")
    parser.add_argument("--output", "-o", required=True, help="Output directory for line art & metadata")
    parser.add_argument("--aspect-ratio", "-a", default="original", choices=["original", "1:1", "4:5", "3:4", "16:9"], help="Crop aspect ratio")
    parser.add_argument("--detail", "-d", type=float, default=0.5, help="Detail level: 0.0 (Junior/Minimal) to 1.0 (Adult/Advanced)")
    parser.add_argument("--publish", "-p", action="store_true", help="Publish converted pages directly to Gumroad")

    args = parser.parse_args()
    process_batch(
        input_dir=args.input,
        output_dir=args.output,
        aspect_ratio=args.aspect_ratio,
        detail_level=args.detail,
        publish_gumroad=args.publish
    )
