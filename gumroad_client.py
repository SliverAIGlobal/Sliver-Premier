import os
import io
import logging
import requests
from typing import Dict, List, Optional, Any, Union

logger = logging.getLogger("GumroadPublisher")

class GumroadPublisher:
    """Official Gumroad API v2 Publisher, Deduplication Engine, File Attacher, and License Client."""

    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or os.getenv("GUMROAD_ACCESS_TOKEN")
        self.base_url = "https://api.gumroad.com/v2"
        self.products_endpoint = f"{self.base_url}/products"
        self._cached_products: Optional[Dict[str, Any]] = None

    def get_existing_product_names(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Fetches all existing storefront products to detect and prevent duplicates."""
        if not self.access_token:
            return {}

        if self._cached_products is not None and not force_refresh:
            return self._cached_products

        try:
            res = requests.get(self.products_endpoint, params={"access_token": self.access_token}, timeout=10)
            data = res.json()
            if data.get("success"):
                products = data.get("products", [])
                # Map lowercase normalized names to product records
                self._cached_products = {p.get("name", "").strip().lower(): p for p in products}
                return self._cached_products
        except Exception as e:
            logger.warning(f"Failed to fetch existing products for deduplication: {e}")

        return {}

    def upload_image_asset(self, image_data: Union[bytes, str], filename: str = "coloring_page.png") -> Optional[str]:
        """Uploads converted line-art PNG through Gumroad S3 presign multipart flow."""
        if not self.access_token:
            return None

        try:
            if isinstance(image_data, str) and os.path.exists(image_data):
                with open(image_data, "rb") as f:
                    file_bytes = f.read()
            elif isinstance(image_data, bytes):
                file_bytes = image_data
            else:
                return None

            file_size = len(file_bytes)
            if file_size == 0:
                return None

            # 1. POST /files/presign
            presign_res = requests.post(f"{self.base_url}/files/presign", data={
                "access_token": self.access_token,
                "filename": filename,
                "content_type": "image/png",
                "file_size": file_size
            }, timeout=12)
            presign_data = presign_res.json()

            if not presign_data.get("success"):
                logger.warning(f"Presign failed: {presign_data}")
                return None

            parts = presign_data.get("parts", [])
            if not parts:
                return None

            part_url = parts[0].get("presigned_url")
            upload_id = presign_data.get("upload_id")
            key = presign_data.get("key")

            # 2. PUT part to S3 presigned URL
            s3_res = requests.put(part_url, data=file_bytes, headers={"Content-Type": "image/png"}, timeout=30)
            etag = s3_res.headers.get("ETag")
            if not etag:
                return None

            # 3. POST /files/complete
            comp_res = requests.post(f"{self.base_url}/files/complete", data={
                "access_token": self.access_token,
                "key": key,
                "upload_id": upload_id,
                "parts[][part_number]": 1,
                "parts[][etag]": etag
            }, timeout=15)
            comp_data = comp_res.json()

            if comp_data.get("success"):
                file_url = comp_data.get("file_url")
                logger.info(f"Image asset successfully uploaded to Gumroad: {file_url}")
                return file_url

        except Exception as e:
            logger.warning(f"Asset upload error: {e}")

        return None

    def publish_product(
        self,
        name: str,
        price_cents: int = 399,
        description: str = "",
        tags: Optional[List[str]] = None,
        image_asset: Optional[Union[bytes, str]] = None,
        promo_code: str = "SUBSCRIBE50",
        discount_percent: int = 50,
        prevent_duplicates: bool = True
    ) -> Dict[str, Any]:
        """Creates product on Gumroad with automatic deduplication, file attachment, and license keys."""

        # 1. Deduplication check
        if prevent_duplicates and self.access_token:
            existing = self.get_existing_product_names()
            norm_name = name.strip().lower()
            if norm_name in existing:
                prev = existing[norm_name]
                logger.info(f"Duplicate product detected: '{name}'. Reusing existing listing.")
                return {
                    "success": True,
                    "duplicate": True,
                    "mode": "live",
                    "product_id": prev.get("id"),
                    "product_url": prev.get("short_url") or prev.get("landing_url"),
                    "price": f"${prev.get('price', price_cents) / 100:.2f}",
                    "is_licensed": True,
                    "promo_code": promo_code,
                    "discount": f"{discount_percent}% OFF",
                    "message": f"Listing already exists on Gumroad ({prev.get('short_url')}). Prevented duplicate upload."
                }

        # Offline Mock Mode
        if not self.access_token or self.access_token.strip() == "":
            mock_id = f"prod_mock_{abs(hash(name)) % 10000000}"
            return {
                "success": True,
                "duplicate": False,
                "mode": "mock",
                "product_id": mock_id,
                "product_url": f"https://sliverai.gumroad.com/l/{mock_id}",
                "price": f"${price_cents / 100:.2f}",
                "is_licensed": True,
                "promo_code": promo_code,
                "discount": f"{discount_percent}% OFF",
                "message": "Mock listing successful. Set GUMROAD_ACCESS_TOKEN to enable real publishing."
            }

        # Live Gumroad Publishing
        try:
            full_description = description or (
                "Official 2026 Color World printable coloring page template. "
                "Includes commercial distribution license key and high-resolution line art. "
                "Use promo code SUBSCRIBE50 for 50% OFF!"
            )

            # Upload coloring image asset if provided
            uploaded_file_url = None
            if image_asset:
                uploaded_file_url = self.upload_image_asset(image_asset, filename=f"{name[:30].replace(' ', '_')}.png")

            payload = [
                ("access_token", self.access_token),
                ("name", name),
                ("price", str(price_cents)),
                ("price_cents", str(price_cents)),
                ("description", full_description),
                ("is_licensed", "true")
            ]

            if tags:
                for t in tags:
                    payload.append(("tags[]", t))

            response = requests.post(self.products_endpoint, data=payload, timeout=15)
            res_data = response.json()

            if not res_data.get("success"):
                error_msg = res_data.get("message", "Unknown API error")
                logger.error(f"API Error: {error_msg}")
                return {"success": False, "error": error_msg}

            product = res_data.get("product", {})
            product_id = product.get("id")
            product_url = product.get("short_url") or product.get("landing_url")

            # Attach uploaded image file to product
            if product_id and uploaded_file_url:
                try:
                    update_payload = {
                        "access_token": self.access_token,
                        "files[][url]": uploaded_file_url
                    }
                    requests.put(f"{self.products_endpoint}/{product_id}", data=update_payload, timeout=12)
                except Exception as e:
                    logger.warning(f"Failed to attach file to product: {e}")

            # Attach promo code offer
            if product_id:
                try:
                    promo_url = f"{self.products_endpoint}/{product_id}/offer_codes"
                    promo_payload = {
                        "access_token": self.access_token,
                        "name": promo_code,
                        "percent_off": discount_percent
                    }
                    requests.post(promo_url, data=promo_payload, timeout=10)
                except Exception:
                    pass

            # Update cache
            if self._cached_products is not None:
                self._cached_products[name.strip().lower()] = product

            return {
                "success": True,
                "duplicate": False,
                "mode": "live",
                "product_id": product_id,
                "product_url": product_url,
                "price": f"${price_cents / 100:.2f}",
                "is_licensed": True,
                "promo_code": promo_code,
                "discount": f"{discount_percent}% OFF",
                "image_attached": bool(uploaded_file_url)
            }

        except Exception as e:
            logger.exception("Failed to connect to API")
            return {"success": False, "error": str(e)}

    def publish_trending_bundle(self, image_asset: Optional[Union[bytes, str]] = None) -> Dict[str, Any]:
        """Publishes the $49.99 Trending Ten Bundle with native license key and SUBSCRIBE50 promo code."""
        return self.publish_product(
            name="2026 Color World: Trending Ten Commercial Bundle",
            price_cents=4999,
            description="The complete 10-volume flagship coloring collection with universal commercial distribution license key. Includes botanical anatomy, fantasy realms, cyberpunk neon, cozy hygge, and corporate training guides. 50% OFF promo code SUBSCRIBE50.",
            tags=["trending bundle", "coloring collection", "commercial license", "line art", "2026 color world", "instant download"],
            image_asset=image_asset,
            promo_code="SUBSCRIBE50",
            discount_percent=50
        )

    def publish_corporate_license(self, image_asset: Optional[Union[bytes, str]] = None) -> Dict[str, Any]:
        """Publishes the $5,000 Corporate White Label Lifetime Training License with unlimited usage."""
        return self.publish_product(
            name="2026 Color World: Corporate White Label Lifetime Training License",
            price_cents=500000,
            description="One-time $5,000 corporate purchase for unlimited lifetime enterprise usage. Includes standalone zero-dependency corporate HTML training engine, custom corporate letterhead/logo upload, branded corporate copyright footer stamping, and employee manual diagram conversions.",
            tags=["corporate training", "white label", "employee manual", "enterprise license", "2026 color world", "compliance"],
            image_asset=image_asset,
            promo_code="ENTERPRISE50",
            discount_percent=50
        )

    def publish_creator_wallpaper(
        self,
        title: str,
        artist_name: str,
        collection_source: str,
        price_usd: float = 4.99,
        precision_score: float = 95.0,
        is_original_upload: bool = False,
        wallpaper_image_bytes: Optional[bytes] = None,
        animated_mp4_bytes: Optional[bytes] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Publish a user-finished static/animated phone wallpaper as a derivative work.
        - Precision gating: Requires Gold (95%+) to qualify for marketplace listing.
        - Attribution requirement: 'Original artwork © 2026 Color World · Colored by {artist_name}'
        - Split: 15% platform commission to Color World if based on standard collections; 0% if original photo upload.
        """
        if precision_score < 95.0:
            raise ValueError(f"Quality gate requirement unmet: Precision score is {precision_score:.1f}%. Gold Tier (95%+) required to list on Creator Marketplace.")

        commission_rate = 0.0 if is_original_upload else 0.15
        cw_cut = round(price_usd * commission_rate, 2)
        artist_payout = round(price_usd - cw_cut, 2)
        price_cents = int(round(price_usd * 100))

        attribution = f"Original artwork © 2026 Color World · Colored & Rendered by {artist_name}"
        desc = (
            f"{title}\n\n"
            f"📱 Ultra High-Res Animated & Static Phone Wallpaper Edition\n"
            f"🎨 {attribution}\n"
            f"✨ Collection Lineage: {collection_source}\n"
            f"🏆 Certified Gold Precision Score: {precision_score:.1f}%\n\n"
            f"Includes:\n"
            f"- Ultra-clarity static 4K phone wallpaper (PNG)\n"
            f"- Seamless organic watercolor ink-bleed dynamic live wallpaper (MP4 / WebM)\n"
            f"- Commercial derivative usage license key\n\n"
            f"Platform Terms: {commission_rate*100:.0f}% platform fee to Color World, ${(artist_payout):.2f} net creator payout. Powered by Color World 2026."
        )

        default_tags = ["phone wallpaper", "live wallpaper", "animated wallpaper", "digital art", "color world", "kawaii winter"]
        final_tags = (tags or default_tags)[:6]

        result = self.publish_product(
            name=f"{title} (Wallpaper Edition)",
            price_cents=price_cents,
            description=desc,
            tags=final_tags,
            image_asset=wallpaper_image_bytes
        )
        result["creator_royalty"] = {
            "artist_name": artist_name,
            "attribution": attribution,
            "commission_rate_percent": commission_rate * 100,
            "platform_cut_usd": cw_cut,
            "artist_payout_usd": artist_payout,
            "certified_precision": precision_score,
            "is_original_upload": is_original_upload
        }
        return result

    # ==========================================
    # Gumroad License Verification & Management
    # ==========================================

    def verify_license(self, product_id: str, license_key: str, increment_uses_count: bool = True) -> Dict[str, Any]:
        """POST /licenses/verify - Verify customer license key."""
        if not self.access_token:
            return {
                "success": True,
                "uses": 1,
                "mode": "mock",
                "purchase": {
                    "product_id": product_id,
                    "license_key": license_key,
                    "price": 399,
                    "refunded": False,
                    "disputed": False,
                    "chargebacked": False
                }
            }

        url = f"{self.base_url}/licenses/verify"
        payload = {
            "product_id": product_id,
            "license_key": license_key,
            "increment_uses_count": "true" if increment_uses_count else "false"
        }
        res = requests.post(url, data=payload, timeout=10)
        return res.json()

    def enable_license(self, product_id: str, license_key: str) -> Dict[str, Any]:
        """PUT /licenses/enable - Enable a customer license."""
        if not self.access_token:
            return {"success": True, "mode": "mock", "product_id": product_id, "license_key": license_key}

        url = f"{self.base_url}/licenses/enable"
        payload = {
            "access_token": self.access_token,
            "product_id": product_id,
            "license_key": license_key
        }
        res = requests.put(url, data=payload, timeout=10)
        return res.json()

    def disable_license(self, product_id: str, license_key: str) -> Dict[str, Any]:
        """PUT /licenses/disable - Disable a customer license."""
        if not self.access_token:
            return {"success": True, "mode": "mock", "product_id": product_id, "license_key": license_key}

        url = f"{self.base_url}/licenses/disable"
        payload = {
            "access_token": self.access_token,
            "product_id": product_id,
            "license_key": license_key
        }
        res = requests.put(url, data=payload, timeout=10)
        return res.json()

    def decrement_license_uses(self, product_id: str, license_key: str) -> Dict[str, Any]:
        """PUT /licenses/decrement_uses_count - Decrement license uses count."""
        if not self.access_token:
            return {"success": True, "mode": "mock", "product_id": product_id, "license_key": license_key}

        url = f"{self.base_url}/licenses/decrement_uses_count"
        payload = {
            "access_token": self.access_token,
            "product_id": product_id,
            "license_key": license_key
        }
        res = requests.put(url, data=payload, timeout=10)
        return res.json()

    def rotate_license(self, product_id: str, license_key: str) -> Dict[str, Any]:
        """PUT /licenses/rotate - Rotate an existing customer license key."""
        if not self.access_token:
            return {
                "success": True,
                "mode": "mock",
                "product_id": product_id,
                "new_license_key": "MOCK-NEW-" + license_key
            }

        url = f"{self.base_url}/licenses/rotate"
        payload = {
            "access_token": self.access_token,
            "product_id": product_id,
            "license_key": license_key
        }
        res = requests.put(url, data=payload, timeout=10)
        return res.json()

    # ==========================================
    # Financial: Payouts & Earnings
    # ==========================================

    def get_earnings(self, year: int) -> Dict[str, Any]:
        """GET /earnings - Retrieve annual earnings breakdown."""
        if not self.access_token:
            return {
                "success": True,
                "year": year,
                "currency": "usd",
                "gross_cents": 39900,
                "fees_cents": 3990,
                "taxes_cents": 0,
                "affiliate_credit_cents": 0,
                "net_cents": 35910
            }

        url = f"{self.base_url}/earnings"
        params = {"access_token": self.access_token, "year": year}
        res = requests.get(url, params=params, timeout=10)
        return res.json()

    def get_payouts(self, before: Optional[str] = None, after: Optional[str] = None) -> Dict[str, Any]:
        """GET /payouts - Retrieves payouts list."""
        if not self.access_token:
            return {
                "success": True,
                "payouts": [
                    {
                        "id": None,
                        "amount": "399.00",
                        "currency": "USD",
                        "status": "payable",
                        "payment_processor": "stripe"
                    }
                ]
            }

        url = f"{self.base_url}/payouts"
        params = {"access_token": self.access_token}
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        res = requests.get(url, params=params, timeout=10)
        return res.json()
