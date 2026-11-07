import io
import base64
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

    def test_catalog_collections_endpoint(self):
        """Test GET /api/catalog/collections returns Junior and Adult curated collections."""
        res = self.client.get("/api/catalog/collections")
        self.assertEqual(res.status_code, 200)
        json_data = res.json()
        self.assertTrue(json_data["success"])
        self.assertIn("junior", json_data["collections"])
        self.assertIn("adult", json_data["collections"])
        self.assertIn("palettes", json_data)
        self.assertIn("textures", json_data)

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
        self.assertIn("COLORWORLD", res_main.text)
        self.assertIn("KAWAII WINTER 2026", res_main.text)
        self.assertIn("SUBSCRIBE50", res_main.text)

        res_corp = self.client.get("/corporate")
        self.assertEqual(res_corp.status_code, 200)
        self.assertIn("Corporate White Label", res_corp.text)

        res_tt = self.client.get("/tiktok")
        self.assertEqual(res_tt.status_code, 200)
        self.assertIn("TikTok", res_tt.text)
        self.assertIn("TikTok Safe-Zone", res_tt.text)

    def test_tiktok_render_gif_endpoint(self):
        """Test POST /api/tiktok/render-gif returns looping GIF bytes."""
        # Create small test data URL
        img = np.full((100, 100, 3), 255, dtype=np.uint8)
        cv2.circle(img, (50, 50), 30, (0, 0, 0), 2)
        _, buf = cv2.imencode(".png", img)
        b64 = base64.b64encode(buf.tobytes()).decode("utf-8")
        data_url = f"data:image/png;base64,{b64}"

        payload = {
            "image_data_url": data_url,
            "preset": "zoom_punch",
            "duration_sec": 1.0,
            "hook_text": "Wait for the end... 🤯",
            "bg_style": "aurora"
        }
        res = self.client.post("/api/tiktok/render-gif", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers["content-type"], "image/gif")
        self.assertGreater(len(res.content), 1000)

    def test_creator_wallpaper_publishing_gold_gate(self):
        """Test Creator Wallpaper publishing Gold Precision (95%+) quality gating and royalty computation."""
        # Below 95% precision should be blocked by quality gate
        fail_res = self.client.post("/api/publish/creator-wallpaper", json={
            "title": "Low Precision Art",
            "artist_name": "Novice",
            "collection_source": "KAWAII WINTER 2026",
            "price_usd": 4.99,
            "precision_score": 82.5,
            "is_original_upload": False
        })
        self.assertEqual(fail_res.status_code, 400)
        self.assertIn("Quality gate requirement unmet", fail_res.json()["detail"])

        # At or above 95% precision passes quality gate and computes royalty
        pass_res = self.client.post("/api/publish/creator-wallpaper", json={
            "title": "Snow Unicorn Prismatic Aurora",
            "artist_name": "Studio Master",
            "collection_source": "KAWAII WINTER 2026",
            "price_usd": 4.99,
            "precision_score": 96.8,
            "is_original_upload": False
        })
        self.assertEqual(pass_res.status_code, 200)
        data = pass_res.json()
        self.assertTrue(data["success"])
        self.assertIn("creator_royalty", data)
        self.assertEqual(data["creator_royalty"]["artist_name"], "Studio Master")
        self.assertEqual(data["creator_royalty"]["commission_rate_percent"], 15.0)
        self.assertEqual(data["creator_royalty"]["artist_payout_usd"], 4.24)
        self.assertIn("Original artwork © 2026 Color World", data["creator_royalty"]["attribution"])

if __name__ == "__main__":
    unittest.main()
