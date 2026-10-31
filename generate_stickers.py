import json

stickers = [
    {
        "id": "stars",
        "name": "⭐ Stars & Magic",
        "count": 10,
        "items": [
            {"name": "Gold Star", "emoji": "⭐", "symbol": "★", "id": "star-gold"},
            {"name": "Glowing Star", "emoji": "🌟", "symbol": "✦", "id": "star-glow"},
            {"name": "Sparkles", "emoji": "✨", "symbol": "✧", "id": "sparkles"},
            {"name": "Dizzy Star", "emoji": "💫", "symbol": "✴", "id": "star-dizzy"},
            {"name": "Lightning", "emoji": "⚡", "symbol": "⚡", "id": "lightning"},
            {"name": "Crescent Moon", "emoji": "🌙", "symbol": "☽", "id": "moon"},
            {"name": "Sun Radiance", "emoji": "☀️", "symbol": "☼", "id": "sun"},
            {"name": "Rainbow Arc", "emoji": "🌈", "symbol": "⌒", "id": "rainbow"},
            {"name": "Magic Crystal", "emoji": "🔮", "symbol": "◆", "id": "crystal"},
            {"name": "Magic Wand", "emoji": "🪄", "symbol": "⚚", "id": "wand"}
        ]
    },
    {
        "id": "animals",
        "name": "🐾 Cute Animals",
        "count": 10,
        "items": [
            {"name": "Kitty Cat", "emoji": "🐱", "symbol": "🐈", "id": "kitty"},
            {"name": "Puppy Dog", "emoji": "🐶", "symbol": "🐕", "id": "puppy"},
            {"name": "Cuddly Bear", "emoji": "🐻", "symbol": "🧸", "id": "bear"},
            {"name": "Fluffy Bunny", "emoji": "🐰", "symbol": "🐇", "id": "bunny"},
            {"name": "Clever Fox", "emoji": "🦊", "symbol": "🦝", "id": "fox"},
            {"name": "Sweet Panda", "emoji": "🐼", "symbol": "🐼", "id": "panda"},
            {"name": "Little Lion", "emoji": "🦁", "symbol": "🦁", "id": "lion"},
            {"name": "Playful Tiger", "emoji": "🐯", "symbol": "🐅", "id": "tiger"},
            {"name": "Magic Unicorn", "emoji": "🦄", "symbol": "🦄", "id": "unicorn"},
            {"name": "Paw Prints", "emoji": "🐾", "symbol": "🐾", "id": "paws"}
        ]
    },
    {
        "id": "snacks",
        "name": "🍦 Yummy Snacks",
        "count": 10,
        "items": [
            {"name": "Ice Cream Cone", "emoji": "🍦", "symbol": "🍨", "id": "ice-cream"},
            {"name": "Cheesy Pizza", "emoji": "🍕", "symbol": "🍕", "id": "pizza"},
            {"name": "Sweet Donut", "emoji": "🍩", "symbol": "🍩", "id": "donut"},
            {"name": "Juicy Burger", "emoji": "🍔", "symbol": "🍔", "id": "burger"},
            {"name": "Movie Popcorn", "emoji": "🍿", "symbol": "🍿", "id": "popcorn"},
            {"name": "Ripe Strawberry", "emoji": "🍓", "symbol": "🍓", "id": "strawberry"},
            {"name": "Cool Watermelon", "emoji": "🍉", "symbol": "🍉", "id": "watermelon"},
            {"name": "Frosted Cupcake", "emoji": "🧁", "symbol": "🧁", "id": "cupcake"},
            {"name": "Boba Bubble Tea", "emoji": "🧋", "symbol": "🧋", "id": "boba"},
            {"name": "Candy Lollipop", "emoji": "🍭", "symbol": "🍭", "id": "lollipop"}
        ]
    },
    {
        "id": "toys",
        "name": "🚀 Toys & Gadgets",
        "count": 10,
        "items": [
            {"name": "Space Rocket", "emoji": "🚀", "symbol": "🚀", "id": "rocket"},
            {"name": "Flying Saucer UFO", "emoji": "🛸", "symbol": "🛸", "id": "ufo"},
            {"name": "Turbo Race Car", "emoji": "🏎️", "symbol": "🏎", "id": "racecar"},
            {"name": "Friendly Robot", "emoji": "🤖", "symbol": "🤖", "id": "robot"},
            {"name": "Royal Crown", "emoji": "👑", "symbol": "♕", "id": "crown"},
            {"name": "Party Balloon", "emoji": "🎈", "symbol": "🎈", "id": "balloon"},
            {"name": "Gift Box", "emoji": "🎁", "symbol": "🎁", "id": "gift"},
            {"name": "Gold Trophy", "emoji": "🏆", "symbol": "🏆", "id": "trophy"},
            {"name": "Sparkle Diamond", "emoji": "💎", "symbol": "💎", "id": "diamond"},
            {"name": "Toy Plane", "emoji": "✈️", "symbol": "✈", "id": "plane"}
        ]
    },
    {
        "id": "moods",
        "name": "💖 Expressive Moods",
        "count": 10,
        "items": [
            {"name": "Glitter Hearts", "emoji": "💖", "symbol": "♥", "id": "sparkle-heart"},
            {"name": "Cool Sunglasses", "emoji": "😎", "symbol": "🕶", "id": "sunglasses"},
            {"name": "Party Celebration Face", "emoji": "🥳", "symbol": "🎉", "id": "party-face"},
            {"name": "Starry Eyes", "emoji": "🤩", "symbol": "★", "id": "star-eyes"},
            {"name": "Pink Cherry Blossom", "emoji": "🌸", "symbol": "🌸", "id": "cherry-blossom"},
            {"name": "Hawaiian Hibiscus", "emoji": "🌺", "symbol": "🌺", "id": "hibiscus"},
            {"name": "Peace Sign", "emoji": "✌️", "symbol": "✌", "id": "peace"},
            {"name": "Happy Tears Joy", "emoji": "😂", "symbol": "☺", "id": "laugh"},
            {"name": "Big Hugs", "emoji": "🤗", "symbol": "♡", "id": "hug"},
            {"name": "Blowing Love Kiss", "emoji": "😘", "symbol": "💋", "id": "kiss"}
        ]
    },
    {
        "id": "nature",
        "name": "🦖 Dinos & Nature",
        "count": 10,
        "items": [
            {"name": "T-Rex Head", "emoji": "🦖", "symbol": "🦖", "id": "dino-rex"},
            {"name": "Tropical Palm Tree", "emoji": "🌴", "symbol": "🌴", "id": "palm-tree"},
            {"name": "Spiral Seashell", "emoji": "🐚", "symbol": "🐚", "id": "seashell"},
            {"name": "Surfing Ocean Wave", "emoji": "🌊", "symbol": "🌊", "id": "wave"},
            {"name": "Forest Mushroom", "emoji": "🍄", "symbol": "🍄", "id": "mushroom"},
            {"name": "Busy Honeybee", "emoji": "🐝", "symbol": "🐝", "id": "bee"},
            {"name": "Flutter Butterfly", "emoji": "🦋", "symbol": "🦋", "id": "butterfly"},
            {"name": "Fiery Volcano", "emoji": "🌋", "symbol": "🌋", "id": "volcano"},
            {"name": "Desert Cactus", "emoji": "🌵", "symbol": "🌵", "id": "cactus"},
            {"name": "Four-Leaf Clover", "emoji": "🍀", "symbol": "🍀", "id": "clover"}
        ]
    }
]

content = f"""// Sliver Kids WASM Coloring Studio v2 ULTRA - 60 Magic Sticker Stamps Dataset
// 6 Categories x 10 Stickers = 60 Interactive Stickers
export const STICKER_CATEGORIES = {json.dumps(stickers, indent=2)};

/**
 * Stamp Sticker onto Canvas
 */
export function drawSticker(ctx, sticker, x, y, size = 48) {{
  ctx.save();
  ctx.font = `${{size}}px "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(sticker.emoji, x, y);
  ctx.restore();
}}
"""

with open("stickers-data.js", "w") as f:
    f.write(content)

print("stickers-data.js generated successfully")
