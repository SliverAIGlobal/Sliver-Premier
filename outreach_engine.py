import os
import json
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("ViralOutreachEngine")

class ViralOutreachEngine:
    """Generates aesthetically tuned viral promotional posts, TikTok/Reels captions, and delegated multi-platform social outreach for completed coloring pages."""

    def __init__(self, storefront_url: str = "https://sliverai.gumroad.com", promo_code: str = "SUBSCRIBE50"):
        self.storefront_url = storefront_url
        self.promo_code = promo_code

    def generate_viral_campaign(
        self,
        template_name: str,
        category: str = "General",
        product_url: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Creates high-conversion viral campaign copy for TikTok, Instagram Reels, Pinterest, YouTube Shorts, and X/Twitter."""
        link = product_url or f"{self.storefront_url}/l/{template_name.lower().replace(' ', '-')}"
        tags_list = tags or [category.lower(), "coloring", "relaxing", "satisfying", "art", "2026colorworld"]
        hashtags_str = " ".join([f"#{t.replace(' ', '')}" for t in tags_list])

        tiktok_caption = (
            f"✨ Watch this black & white sketch come to life with watercolor ink bleed! 🎨💧 "
            f"Download '{template_name}' instantly ({link}). "
            f"Use code {self.promo_code} for 50% OFF! Like & follow for daily relaxing coloring art! "
            f"{hashtags_str} #inkbleed #satisfying #oddlysatisfying #coloringpage"
        )

        instagram_caption = (
            f"From raw ink contours to vibrant chromatic bloom ✨🌿\n\n"
            f"Template: {template_name}\n"
            f"Collection: 2026 Color World ({category})\n"
            f"⚡ Direct Link in bio or visit: {link}\n"
            f"🏷️ Take 50% OFF with commercial usage rights: '{self.promo_code}'\n\n"
            f"Double tap if this ink flow brought your mind peace today 🧘‍♀️🖌️\n\n"
            f"{hashtags_str} #watercolorbleed #adultcoloring #zenart #coloringtherapy"
        )

        pinterest_pin = {
            "title": f"Aesthetic {template_name} Coloring Page (Instant Download PDF)",
            "description": f"Printable coloring template with high-resolution line art. Watch the mesmerizing ink-bleed coloring process video! Get commercial license on Gumroad with code {self.promo_code} for 50% discount.",
            "destination_url": link,
            "tags": tags_list + ["printable coloring", "diy art", "stress relief"]
        }

        youtube_shorts = {
            "title": f"Aesthetic Watercolor Ink-Bleed 🖌️ {template_name} #shorts",
            "description": (
                f"Watch black & white line art turn into rich glowing watercolor in this relaxing completion video.\n"
                f"📥 Download the full printable coloring template: {link}\n"
                f"🎟️ 50% discount coupon: {self.promo_code}\n"
                f"Stamped official © 2026 Color World."
            ),
            "tags": tags_list + ["shorts", "artshorts", "relaxingart"]
        }

        twitter_post = (
            f"🎨 New printable release: '{template_name}'\n"
            f"Sub-50ms line-art rendering with commercial copyright license.\n\n"
            f"Watch the ink bleed transformation 👇\n"
            f"Claim 50% OFF with code {self.promo_code}: {link}\n\n"
            f"#ColoringPage #DigitalArt #RelaxingArt"
        )

        email_outreach = {
            "subject": f"🎨 New Aesthetic Coloring Drop: {template_name} (50% VIP Secret Code)",
            "body": (
                f"Hi Color World VIP,\n\n"
                f"We just dropped a brand new coloring template in our {category} collection: '{template_name}'.\n\n"
                f"Our new ink-bleed video rendering engine converts black and white line art into flowing watercolor in seconds. "
                f"You can now download the high-resolution printable PDF directly from our Gumroad storefront.\n\n"
                f"Grab your copy today with our 50% OFF subscriber coupon: {self.promo_code}\n"
                f"Instant Access: {link}\n\n"
                f"Happy coloring,\n"
                f"The 2026 Color World Team"
            )
        }

        sms_blast = (
            f"Color World VIP: New {template_name} coloring page is live! "
            f"Watch the viral ink-bleed clip & get 50% OFF with code {self.promo_code}: {link}"
        )

        return {
            "template_name": template_name,
            "product_url": link,
            "promo_code": self.promo_code,
            "platforms": {
                "tiktok": tiktok_caption,
                "instagram_reels": instagram_caption,
                "pinterest": pinterest_pin,
                "youtube_shorts": youtube_shorts,
                "twitter_x": twitter_post,
                "email_campaign": email_outreach,
                "sms_blast": sms_blast
            }
        }
