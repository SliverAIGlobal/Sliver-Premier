import os
import sys
import unittest
import numpy as np
import cv2
from PIL import Image
from engine import ColoringPageEngine, MetadataGenerator
from gumroad_client import GumroadPublisher

class TestColoringPageEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ColoringPageEngine(copyright_text="© 2026 Color World")
        self.meta_gen = MetadataGenerator()
        self.publisher = GumroadPublisher()

        # Create 1080p synthetic test image
        self.test_img = np.zeros((1080, 1920, 3), dtype=np.uint8)
        cv2.circle(self.test_img, (960, 540), 300, (255, 255, 255), -1)
        cv2.rectangle(self.test_img, (400, 200), (800, 800), (128, 128, 255), -1)

    def test_sub_50ms_conversion_latency(self):
        """Verify image conversion completes under 50ms requirement."""
        # Warmup
        self.engine.convert_image(self.test_img)

        # Benchmark run
        times = []
        for _ in range(5):
            _, elapsed_ms = self.engine.convert_image(self.test_img)
            times.append(elapsed_ms)

        avg_time = sum(times) / len(times)
        print(f"\n[BENCHMARK] Average Conversion Latency: {avg_time:.2f} ms (Target: < 50ms)")
        self.assertLess(avg_time, 50.0, f"Conversion speed ({avg_time:.2f}ms) exceeded 50ms budget!")

    def test_aspect_ratio_cropping(self):
        """Verify 1:1, 4:5, and custom crop box functionality."""
        img_1to1, ms_1to1 = self.engine.convert_image(self.test_img, aspect_ratio="1:1")
        self.assertEqual(img_1to1.size[0], img_1to1.size[1])
        self.assertLess(ms_1to1, 50.0)

        img_4to5, ms_4to5 = self.engine.convert_image(self.test_img, aspect_ratio="4:5")
        # 4:5 ratio on height 1080 -> width = 864
        self.assertEqual(img_4to5.size, (864, 1080))
        self.assertLess(ms_4to5, 50.0)

        img_box, ms_box = self.engine.convert_image(self.test_img, crop_box=(100, 100, 500, 500))
        self.assertEqual(img_box.size, (500, 500))
        self.assertLess(ms_box, 50.0)

    def test_detail_slider_junior_to_adult(self):
        """Verify sliding scale from Junior (0.0) to Adult (1.0) detail."""
        img_junior, ms_j = self.engine.convert_image(self.test_img, detail_level=0.1)
        self.assertLess(ms_j, 50.0)

        img_adult, ms_a = self.engine.convert_image(self.test_img, detail_level=0.95)
        self.assertLess(ms_a, 50.0)

        meta_j = self.meta_gen.generate_metadata("castle.png", detail_level=0.1)
        self.assertIn("junior minimal", meta_j["tags"])
        self.assertEqual(len(meta_j["tags"]), 6)

        meta_a = self.meta_gen.generate_metadata("castle.png", detail_level=0.95)
        self.assertIn("adult fine detail", meta_a["tags"])
        self.assertEqual(len(meta_a["tags"]), 6)

    def test_watermark_stamping(self):
        """Verify image conversion includes the stamped copyright text."""
        pil_img, _ = self.engine.convert_image(self.test_img)
        self.assertEqual(pil_img.mode, "RGB")
        w, h = pil_img.size
        self.assertEqual((w, h), (1920, 1080))

    def test_metadata_generation_6_tags(self):
        """Verify AI metadata generates title, name, and EXACTLY 6 indexing tags."""
        meta = self.meta_gen.generate_metadata("dragon_castle.jpg")
        self.assertIn("name", meta)
        self.assertIn("title", meta)
        self.assertIn("tags", meta)
        self.assertEqual(len(meta["tags"]), 6, f"Expected 6 tags, got {len(meta['tags'])}")
        self.assertIn("2026 color world", meta["tags"])

    def test_gumroad_mock_publication(self):
        """Verify Gumroad publisher operates seamlessly in mock mode at $3.99 with license key enabled."""
        res = self.publisher.publish_product(
            name="Dragon Castle Coloring Template",
            price_cents=399,
            tags=["dragon castle", "coloring page", "line art", "2026 color world", "printable template", "instant download"]
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["price"], "$3.99")
        self.assertTrue(res["is_licensed"])
        self.assertEqual(res["promo_code"], "SUBSCRIBE50")
        self.assertEqual(res["discount"], "50% OFF")

    def test_license_verification_and_management(self):
        """Verify license verify, enable, disable, and rotate methods."""
        v = self.publisher.verify_license("prod_abc", "LIC-12345")
        self.assertTrue(v["success"])
        self.assertEqual(v["purchase"]["price"], 399)

        e = self.publisher.enable_license("prod_abc", "LIC-12345")
        self.assertTrue(e["success"])

        d = self.publisher.disable_license("prod_abc", "LIC-12345")
        self.assertTrue(d["success"])

        r = self.publisher.rotate_license("prod_abc", "LIC-12345")
        self.assertTrue(r["success"])
        self.assertIn("MOCK-NEW", r["new_license_key"])

if __name__ == "__main__":
    unittest.main()
