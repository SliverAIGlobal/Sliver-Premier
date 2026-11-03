import io
import unittest
import numpy as np
import cv2
from PIL import Image
from fastapi.testclient import TestClient
from app import app

class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

        # Create dummy PNG image bytes
        img = np.zeros((300, 300, 3), dtype=np.uint8)
        cv2.circle(img, (150, 150), 80, (255, 255, 255), -1)
        _, buf = cv2.imencode(".png", img)
        self.dummy_bytes = buf.tobytes()

    def test_convert_endpoint_and_speed_benchmark(self):
        """Test POST /api/convert returns <50ms benchmark passed and metadata."""
        files = {"file": ("flower_garden.png", io.BytesIO(self.dummy_bytes), "image/png")}
        data = {
            "aspect_ratio": "1:1",
            "detail_level": "0.50"
        }
        res = self.client.post("/api/convert", files=files, data=data)
        self.assertEqual(res.status_code, 200)
        json_data = res.json()

        self.assertTrue(json_data["success"])
        self.assertTrue(json_data["benchmark_passed"])
        self.assertLess(json_data["conversion_ms"], 50.0)
        self.assertIn("data:image/png;base64,", json_data["image_data_url"])

        meta = json_data["metadata"]
        self.assertEqual(len(meta["tags"]), 6)
        self.assertIn("2026 color world", meta["tags"])

    def test_publish_endpoint_mock_and_options(self):
        """Test POST /api/publish succeeds with $3.99 and SUBSCRIBE50 promo code."""
        payload = {
            "name": "Zen Meadow Template",
            "price_cents": 399,
            "tags": ["zen", "meadow", "mindfulness", "line art", "2026 color world", "instant download"],
            "promo_code": "SUBSCRIBE50",
            "prevent_duplicates": True
        }
        res = self.client.post("/api/publish", json=payload)
        self.assertEqual(res.status_code, 200)
        json_data = res.json()
        self.assertTrue(json_data["success"])
        self.assertEqual(json_data["price"], "$3.99")
        self.assertTrue(json_data["is_licensed"])

    def test_products_endpoint(self):
        """Test GET /api/products returns storefront products catalog."""
        res = self.client.get("/api/products")
        self.assertEqual(res.status_code, 200)
        json_data = res.json()
        self.assertTrue(json_data["success"])
        self.assertIn("products", json_data)

    def test_outreach_endpoint(self):
        """Test POST /api/outreach/generate produces multi-platform posts."""
        payload = {
            "template_name": "Lotus Blossom",
            "category": "Botanical",
            "tags": ["botanical", "lotus", "coloring"]
        }
        res = self.client.post("/api/outreach/generate", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("platforms", data)
        self.assertIn("tiktok", data["platforms"])
        self.assertIn("instagram_reels", data["platforms"])

    def test_blog_endpoint(self):
        """Test POST /api/blog/generate produces markdown article with backlinks."""
        payload = {
            "template_name": "Lotus Blossom",
            "category": "Botanical"
        }
        res = self.client.post("/api/blog/generate", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("markdown_content", data)
        self.assertIn("sliverai.gumroad.com", data["markdown_content"])

    def test_license_verify_endpoint(self):
        """Test POST /api/license/verify validates customer licenses."""
        payload = {
            "product_id": "test_prod",
            "license_key": "TEST-LIC-KEY-999"
        }
        res = self.client.post("/api/license/verify", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["success"])

    def test_html_dashboard_routes(self):
        """Test main index.html and corporate dashboard return 200 OK."""
        res_main = self.client.get("/")
        self.assertEqual(res_main.status_code, 200)
        self.assertIn("2026 Color World", res_main.text)
        self.assertIn("Category Filters", res_main.text)
        self.assertIn("SUBSCRIBE50", res_main.text)

        res_corp = self.client.get("/corporate")
        self.assertEqual(res_corp.status_code, 200)
        self.assertIn("Corporate White Label", res_corp.text)

if __name__ == "__main__":
    unittest.main()
