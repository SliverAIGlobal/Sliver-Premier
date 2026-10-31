import json

packs = [
    {
        "id": "dinos",
        "name": "🦖 Dinosaurs & Prehistory",
        "count": 12,
        "items": [
            {"title": "T-Rex King", "desc": "The mighty Tyrannosaurus Rex roaring in the prehistoric jungle", "id": "t-rex"},
            {"title": "Triceratops Friend", "desc": "A friendly three-horned dinosaur smiling by palm ferns", "id": "triceratops"},
            {"title": "Stegosaurus Spikes", "desc": "Armored Stegosaurus with double row back plates", "id": "stegosaurus"},
            {"title": "Pterodactyl Glide", "desc": "Flying pterosaur soaring over prehistoric volcano peaks", "id": "pterodactyl"},
            {"title": "Brachiosaurus Tall", "desc": "Gentle giant long-neck reaching for highest tree leaves", "id": "brachiosaurus"},
            {"title": "Velociraptor Swift", "desc": "Agile feathered raptor running across the savannah", "id": "velociraptor"},
            {"title": "Ankylosaurus Club", "desc": "Heavy armored dino with a giant tail club", "id": "ankylosaurus"},
            {"title": "Parasaurolophus Horn", "desc": "Crest-headed musical herbivore dinosaur", "id": "parasaurolophus"},
            {"title": "Spinosaurus River", "desc": "Giant sail-backed predator wading in the ancient river", "id": "spinosaurus"},
            {"title": "Baby Dino Egg Hatch", "desc": "Cute little dinosaur hatching out of its polka-dot egg", "id": "baby-dino"},
            {"title": "Plesiosaur Sea", "desc": "Prehistoric long-necked sea reptile diving underwater", "id": "plesiosaur"},
            {"title": "Volcano Dino Valley", "desc": "Lava volcano landscape with ancient ferns and dino friends", "id": "dino-valley"}
        ]
    },
    {
        "id": "space",
        "name": "🚀 Space & Galaxy",
        "count": 12,
        "items": [
            {"title": "Rocket Explorer", "desc": "Multi-stage space rocket blasting off with fiery trail", "id": "rocket"},
            {"title": "Astronaut Dog", "desc": "Brave canine astronaut floating in deep zero-gravity space", "id": "astro-dog"},
            {"title": "Saturn & Rings", "desc": "Magnificent gas giant surrounded by luminous rings", "id": "saturn"},
            {"title": "Alien UFO", "desc": "Friendly alien waving from a saucer spaceship", "id": "ufo"},
            {"title": "Lunar Rover", "desc": "Moon buggy vehicle exploring craters on the lunar surface", "id": "lunar-rover"},
            {"title": "Solar System", "desc": "The Sun surrounded by orbiting planets and shooting stars", "id": "solar-system"},
            {"title": "Spacewalk Astronaut", "desc": "Hero astronaut fixing solar panels outside space station", "id": "spacewalk"},
            {"title": "Shooting Star Nebula", "desc": "Twinkling cosmic star shower across glowing nebula clouds", "id": "shooting-star"},
            {"title": "Cosmic Space Station", "desc": "Orbital scientific satellite reflecting starlight", "id": "space-station"},
            {"title": "Mars Explorer Base", "desc": "Futuristic geodesic dome colony on the red planet", "id": "mars-base"},
            {"title": "Friendly Moon", "desc": "Smiling crescent moon wearing a cozy nightcap", "id": "smiling-moon"},
            {"title": "Comet Cruiser", "desc": "Starlight comet sailing past sparkling constellations", "id": "comet"}
        ]
    },
    {
        "id": "ocean",
        "name": "🐬 Ocean Deep",
        "count": 12,
        "items": [
            {"title": "Playful Dolphin", "desc": "Agile dolphin leaping joyfully above sparkling ocean waves", "id": "dolphin"},
            {"title": "Sea Turtle Glide", "desc": "Gentle Hawaiian green sea turtle gliding through coral reefs", "id": "sea-turtle"},
            {"title": "Friendly Octopus", "desc": "Clever eight-armed octopus holding sea treasures and shells", "id": "octopus"},
            {"title": "Coral Reef Life", "desc": "Underwater garden bustling with clownfish and sea anemones", "id": "coral-reef"},
            {"title": "Submarine Quest", "desc": "Yellow research submarine exploring the deep ocean trench", "id": "submarine"},
            {"title": "Humpback Whale", "desc": "Majestic mother whale and baby calf swimming together", "id": "humpback-whale"},
            {"title": "Smiling Jellyfish", "desc": "Translucent bell jellyfish floating with gentle ribbons", "id": "jellyfish"},
            {"title": "Starfish Seafloor", "desc": "Golden starfish resting beside sea shells on white sand", "id": "starfish"},
            {"title": "Seahorse Garden", "desc": "Couple of sea horses clinging onto underwater kelp forest", "id": "seahorse"},
            {"title": "Sunken Treasure Chest", "desc": "Pirate treasure chest overflowing with gems and coins", "id": "treasure-chest"},
            {"title": "Great White Shark", "desc": "Curious smiling shark inspecting colorful schooling fish", "id": "shark"},
            {"title": "Manta Ray Flight", "desc": "Graceful manta ray gliding like underwater wings of peace", "id": "manta-ray"}
        ]
    },
    {
        "id": "safari",
        "name": "🦁 Safari & Jungle Animals",
        "count": 12,
        "items": [
            {"title": "Lion King", "desc": "Proud lion with a golden magnificent mane on Pride Rock", "id": "lion"},
            {"title": "Baby Elephant Splash", "desc": "Playful calf spraying cool water with its curly trunk", "id": "elephant"},
            {"title": "Tall Giraffe", "desc": "Long-necked spotted giraffe nibbling acacia treetops", "id": "giraffe"},
            {"title": "Playful Monkey", "desc": "Cheeky monkey swinging from jungle vines with a banana", "id": "monkey"},
            {"title": "Panda with Bamboo", "desc": "Chubby panda bear munching sweet fresh bamboo shoots", "id": "panda"},
            {"title": "Zebra Stripes", "desc": "Dazzling zebra galloping across the golden savanna grass", "id": "zebra"},
            {"title": "Hippo Lagoon", "desc": "Happy hippopotamus bathing peacefully in the river bend", "id": "hippo"},
            {"title": "Cheetah Dash", "desc": "Fast spotted cheetah sprinting across open plains", "id": "cheetah"},
            {"title": "Koala Tree Nap", "desc": "Cuddly koala bear hugging an eucalyptus tree trunk", "id": "koala"},
            {"title": "Kangaroo Hop", "desc": "Mother kangaroo hopping with baby joey peek-a-boo", "id": "kangaroo"},
            {"title": "Jungle Toucan", "desc": "Colorful big-beaked toucan perched on an exotic branch", "id": "toucan"},
            {"title": "Flamingo Lagoon", "desc": "Graceful pink flamingo standing balance on one slender leg", "id": "flamingo"}
        ]
    },
    {
        "id": "fantasy",
        "name": "🦄 Fairytales & Fantasy",
        "count": 12,
        "items": [
            {"title": "Magical Unicorn", "desc": "Enchanted unicorn with spiral horn and flowing rainbow mane", "id": "unicorn"},
            {"title": "Friendly Fire Dragon", "desc": "Kind winged dragon roasting marshmallows by campfire", "id": "dragon"},
            {"title": "Royal Magic Castle", "desc": "Majestic fairy tale castle with turrets, banners, and moat", "id": "castle"},
            {"title": "Wizard Potions", "desc": "Wise little wizard brewing sparkling star potions in a cauldron", "id": "wizard"},
            {"title": "Flying Pegasus", "desc": "Winged stallion soaring through puffy marshmallow clouds", "id": "pegasus"},
            {"title": "Mermaid Lagoon", "desc": "Beautiful mermaid resting on a sun-warmed ocean rock", "id": "mermaid"},
            {"title": "Enchanted Fairy", "desc": "Tiny woodland fairy dusting flowers with magical glitter", "id": "fairy"},
            {"title": "Crystal Magic Wand", "desc": "Ornate wand shooting starbursts and hearts into the sky", "id": "wand"},
            {"title": "Phoenix Rising", "desc": "Legendary fire bird illuminating the night with plumage", "id": "phoenix"},
            {"title": "Gnome Mushroom House", "desc": "Whimsical forest gnome tending his spotted toadstool home", "id": "gnome-house"},
            {"title": "Knight with Shield", "desc": "Brave knight in shining armor standing guard at castle gate", "id": "knight"},
            {"title": "Wishing Well", "desc": "Stone wishing well surrounded by blooming four-leaf clovers", "id": "wishing-well"}
        ]
    },
    {
        "id": "vehicles",
        "name": "🏎️ Vehicles & Speed",
        "count": 12,
        "items": [
            {"title": "Super Race Car", "desc": "Aerodynamic race car speeding across the checkered finish line", "id": "race-car"},
            {"title": "Fire Engine Rescue", "desc": "Big red ladder fire truck with sirens flashing ready to save", "id": "fire-truck"},
            {"title": "Police Chopper", "desc": "Helicopter with spinning blades patroling over the city skyline", "id": "police-chopper"},
            {"title": "Monster Truck Jam", "desc": "Giant-wheeled monster truck crushing dirt mounds in arena", "id": "monster-truck"},
            {"title": "Supersonic Jet", "desc": "Sleek fighter aircraft breaking the sound barrier in clouds", "id": "jet-aircraft"},
            {"title": "Heavy Digger Excavator", "desc": "Construction excavator scooping big buckets of earth", "id": "excavator"},
            {"title": "High-Speed Train", "desc": "Futuristic bullet train zipping smoothly along tracks", "id": "bullet-train"},
            {"title": "City School Bus", "desc": "Bright yellow school bus smiling with friendly headlight eyes", "id": "school-bus"},
            {"title": "Ocean Cruise Ship", "desc": "Giant passenger ship cruising under sunny blue skies", "id": "cruise-ship"},
            {"title": "Farm Tractor", "desc": "Sturdy green tractor plowing neat rows in the farm field", "id": "tractor"},
            {"title": "Motorcycle Cruiser", "desc": "Classic road motorbike cruising on the open highway", "id": "motorcycle"},
            {"title": "Hot Air Balloon", "desc": "Colorful striped hot air balloon drifting over rolling hills", "id": "hot-air-balloon"}
        ]
    },
    {
        "id": "island",
        "name": "🌺 808 Island Paradise",
        "count": 12,
        "items": [
            {"title": "Aloha Honu Turtle", "desc": "Sacred Hawaiian sea turtle swimming in turquoise shorelines", "id": "aloha-honu"},
            {"title": "Palm Tree Sunset", "desc": "Twin leaning coconut palms framing a warm island sunset", "id": "palm-sunset"},
            {"title": "Hawaiian Hibiscus", "desc": "Vibrant tropical hibiscus bloom with lush rainforest leaves", "id": "hibiscus"},
            {"title": "Outrigger Canoe", "desc": "Traditional Polynesian sailing canoe riding cresting ocean swells", "id": "outrigger-canoe"},
            {"title": "Volcano Peak Haleakala", "desc": "Shield volcano glowing under twinkling island starlight", "id": "volcano-peak"},
            {"title": "Ukulele Melody", "desc": "Wooden four-string ukulele resting next to floral leis", "id": "ukulele"},
            {"title": "Plumeria Lei", "desc": "Fragrant flower garland woven with sweet yellow plumeria", "id": "plumeria-lei"},
            {"title": "Shave Ice Treat", "desc": "Rainbow rainbow-syrup shave ice topped with sweet mochi", "id": "shave-ice"},
            {"title": "Surfer on the Wave", "desc": "Courageous surfer carving the tube of a glassy blue wave", "id": "surfer"},
            {"title": "Tiki Totem Friend", "desc": "Carved wooden tiki statue with wide joyful smile", "id": "tiki-totem"},
            {"title": "Pineapple King", "desc": "Sweet golden island pineapple wearing cool sunglasses", "id": "pineapple"},
            {"title": "Rainbow over Diamond Head", "desc": "Lush island headland arched by a double tropical rainbow", "id": "rainbow-diamond-head"}
        ]
    },
    {
        "id": "robots",
        "name": "🤖 Robots & Future",
        "count": 12,
        "items": [
            {"title": "Helper Bot 9000", "desc": "Friendly domestic assistant robot serving cups of juice", "id": "helper-bot"},
            {"title": "Robot Dog Rover", "desc": "Bionic mechanical puppy wagging antenna tail with joy", "id": "robot-dog"},
            {"title": "Space Mech Titan", "desc": "Giant articulated robotic exosuit protecting space station", "id": "space-mech"},
            {"title": "Eco-Bot Gardener", "desc": "Solar-powered robot planting seedlings and watering flowers", "id": "eco-bot"},
            {"title": "Flying Drone Scout", "desc": "Quad-rotor drone carrying packages through futuristic city", "id": "flying-drone"},
            {"title": "Cyber Cat Neo", "desc": "Metallic kitten playing with a holographic ball of yarn", "id": "cyber-cat"},
            {"title": "Nanotech Builder", "desc": "Microscopic robot constructing crystalline honeycombs", "id": "nanotech-builder"},
            {"title": "Music Synth Bot", "desc": "DJ robot mixing cosmic beats with turntable and headphones", "id": "synth-bot"},
            {"title": "Solar Rover Scout", "desc": "Tracked exploration bot gathering mineral crystals on rocks", "id": "solar-rover"},
            {"title": "Smart Clockwork Owl", "desc": "Mechanical steampunk owl with brass gears and glowing eyes", "id": "clockwork-owl"},
            {"title": "Android Chef", "desc": "Bipedal chef robot flipping pancakes in futuristic kitchen", "id": "android-chef"},
            {"title": "Friendly Hologram", "desc": "Luminous holographic projection saying hello with sparkles", "id": "hologram"}
        ]
    },
    {
        "id": "sweets",
        "name": "🍕 Sweets & Yummy Foods",
        "count": 12,
        "items": [
            {"title": "Happy Pizza Slice", "desc": "Cheesy pizza slice with pepperoni topping and beaming smile", "id": "pizza-slice"},
            {"title": "Ice Cream Tower", "desc": "Triple scoop sundae cone with waffle texture and cherry on top", "id": "ice-cream-tower"},
            {"title": "Sprinkle Donut", "desc": "Frosted glaze donut covered in colorful festive rainbow sprinkles", "id": "donut"},
            {"title": "Boba Milk Tea Cup", "desc": "Delicious milk tea with tapioca pearls and wide straw", "id": "boba-tea"},
            {"title": "Cupcake Stack", "desc": "Swirled frosting cupcake topped with sweet candy stars", "id": "cupcake-stack"},
            {"title": "Fiesta Taco", "desc": "Crispy taco shell stuffed with lettuce, tomatoes, and cheddar", "id": "fiesta-taco"},
            {"title": "Glazed Pancake Stack", "desc": "Tower of golden fluffy pancakes dripping with maple syrup", "id": "pancakes"},
            {"title": "Crispy French Fries", "desc": "Happy bag of golden potato fries waving ketchup dip", "id": "french-fries"},
            {"title": "Juicy Burger", "desc": "Deluxe sesame seed hamburger with fresh veggies and cheese", "id": "burger"},
            {"title": "Popcorn Tub", "desc": "Buttery movie popcorn overflowing from striped carnival bucket", "id": "popcorn"},
            {"title": "Sweet Candy Lollipop", "desc": "Swirled spiral rainbow lollipop on a paper candy stick", "id": "lollipop"},
            {"title": "Fresh Watermelon Slice", "desc": "Juicy triangular slice of summer watermelon with black seeds", "id": "watermelon"}
        ]
    },
    {
        "id": "mandalas",
        "name": "🎨 Mandalas & Patterns",
        "count": 12,
        "items": [
            {"title": "Starburst Wheel", "desc": "Radial mandala featuring eight-pointed stars and symmetry", "id": "starburst-wheel"},
            {"title": "Floral Mosaic", "desc": "Concentric petals blooming outward in geometric harmony", "id": "floral-mosaic"},
            {"title": "Cosmic Swirl", "desc": "Galactic spiral arms dotted with planetary geometric rings", "id": "cosmic-swirl"},
            {"title": "Diamond Lattice", "desc": "Interlocking crystalline diamond facets with inner facets", "id": "diamond-lattice"},
            {"title": "Ocean Wave Mandala", "desc": "Curling cresting waves arranged in circular calm rhythm", "id": "ocean-waves"},
            {"title": "Sun & Moon Harmony", "desc": "Celestial disc balancing daytime solar rays and lunar phases", "id": "sun-moon"},
            {"title": "Sacred Hexagon Hive", "desc": "Honeycomb mandala structured with sacred hexagonal rings", "id": "hexagon-hive"},
            {"title": "Kaleidoscope Bloom", "desc": "Vibrant kaleidoscope pattern with alternating leaf sectors", "id": "kaleidoscope"},
            {"title": "Zen Ripple Lotus", "desc": "Water ripple concentric circles cradling open lotus blossom", "id": "zen-lotus"},
            {"title": "Tribal Geometric Wheel", "desc": "Bold Polynesian chevron and geometric triangle ring", "id": "tribal-wheel"},
            {"title": "Heart Rhythm Spiral", "desc": "Interlaced heart silhouettes spiraling toward the central core", "id": "heart-spiral"},
            {"title": "Lumina Crystal Mandala", "desc": "Multifaceted gemstone star radiating crystalline light paths", "id": "crystal-mandala"}
        ]
    }
]

js_content = f"""// Sliver Kids WASM Coloring Studio v2 ULTRA - 120 Vector Coloring Pages Dataset
// 10 Themed Packs x 12 Pages = 120 Pages
export const COLORING_PACKS = {json.dumps(packs, indent=2)};

/**
 * Procedural Vector Path Outline Renderer
 * Draws clean, black line-art outlines on the canvas for coloring.
 */
export function drawPageVector(ctx, pageId, width, height) {{
  ctx.save();
  ctx.fillStyle = '#FFFFFF';
  ctx.fillRect(0, 0, width, height);

  ctx.strokeStyle = '#000000';
  ctx.fillStyle = '#000000';
  ctx.lineWidth = 4;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';

  const cx = width / 2;
  const cy = height / 2;

  // Outer border with friendly rounded corners
  ctx.beginPath();
  if (ctx.roundRect) {{
    ctx.roundRect(16, 16, width - 32, height - 32, 24);
  }} else {{
    ctx.rect(16, 16, width - 32, height - 32);
  }}
  ctx.stroke();

  // Draw procedural theme-specific geometric coloring outlines
  drawThemeVector(ctx, pageId, cx, cy, width, height);

  ctx.restore();
}}

function drawThemeVector(ctx, pageId, cx, cy, w, h) {{
  const scale = Math.min(w, h) / 500;

  // Ground line or horizon
  ctx.beginPath();
  ctx.moveTo(32, h - 75);
  ctx.lineTo(w - 32, h - 75);
  ctx.stroke();

  // Background decor: Clouds or Stars
  drawCloudsAndStars(ctx, w, h);

  // Main subject outline based on pageId
  if (pageId.includes("dino") || pageId.includes("rex") || pageId.includes("stego") || pageId.includes("raptor") || pageId.includes("saurolophus") || pageId.includes("spino") || pageId.includes("triceratops") || pageId.includes("brachio")) {{
    drawDinosaurBody(ctx, cx, cy, scale);
  }} else if (pageId.includes("rocket") || pageId.includes("astro") || pageId.includes("space") || pageId.includes("saturn") || pageId.includes("ufo") || pageId.includes("moon") || pageId.includes("solar") || pageId.includes("mars") || pageId.includes("comet")) {{
    drawSpaceSubject(ctx, cx, cy, scale);
  }} else if (pageId.includes("dolphin") || pageId.includes("turtle") || pageId.includes("whale") || pageId.includes("octopus") || pageId.includes("shark") || pageId.includes("jelly") || pageId.includes("coral") || pageId.includes("seahorse") || pageId.includes("sub") || pageId.includes("starfish")) {{
    drawOceanSubject(ctx, cx, cy, scale);
  }} else if (pageId.includes("lion") || pageId.includes("elephant") || pageId.includes("giraffe") || pageId.includes("monkey") || pageId.includes("panda") || pageId.includes("zebra") || pageId.includes("hippo") || pageId.includes("cheetah") || pageId.includes("koala") || pageId.includes("kangaroo")) {{
    drawSafariSubject(ctx, cx, cy, scale);
  }} else if (pageId.includes("unicorn") || pageId.includes("dragon") || pageId.includes("castle") || pageId.includes("wizard") || pageId.includes("pegasus") || pageId.includes("mermaid") || pageId.includes("fairy") || pageId.includes("phoenix")) {{
    drawFantasySubject(ctx, cx, cy, scale);
  }} else if (pageId.includes("car") || pageId.includes("truck") || pageId.includes("bus") || pageId.includes("chopper") || pageId.includes("jet") || pageId.includes("train") || pageId.includes("ship") || pageId.includes("tractor") || pageId.includes("balloon")) {{
    drawVehicleSubject(ctx, cx, cy, scale);
  }} else if (pageId.includes("aloha") || pageId.includes("palm") || pageId.includes("hibiscus") || pageId.includes("ukulele") || pageId.includes("lei") || pageId.includes("ice") || pageId.includes("surfer") || pageId.includes("tiki") || pageId.includes("pineapple")) {{
    drawIslandSubject(ctx, cx, cy, scale);
  }} else if (pageId.includes("bot") || pageId.includes("drone") || pageId.includes("mech") || pageId.includes("cyber") || pageId.includes("nano") || pageId.includes("android")) {{
    drawRobotSubject(ctx, cx, cy, scale);
  }} else if (pageId.includes("pizza") || pageId.includes("cream") || pageId.includes("donut") || pageId.includes("boba") || pageId.includes("taco") || pageId.includes("burger") || pageId.includes("cupcake") || pageId.includes("popcorn") || pageId.includes("candy")) {{
    drawFoodSubject(ctx, cx, cy, scale);
  }} else {{
    drawMandalaSubject(ctx, cx, cy, scale);
  }}
}}

function drawCloudsAndStars(ctx, w, h) {{
  // Cloud 1
  ctx.beginPath();
  ctx.arc(80, 80, 24, 0, Math.PI * 2);
  ctx.arc(110, 70, 30, 0, Math.PI * 2);
  ctx.arc(140, 80, 24, 0, Math.PI * 2);
  ctx.stroke();

  // Cloud 2
  ctx.beginPath();
  ctx.arc(w - 120, 90, 28, 0, Math.PI * 2);
  ctx.arc(w - 85, 80, 32, 0, Math.PI * 2);
  ctx.stroke();

  // Sun
  ctx.beginPath();
  ctx.arc(w / 2, 60, 20, 0, Math.PI * 2);
  ctx.stroke();
  for (let a = 0; a < Math.PI * 2; a += Math.PI / 4) {{
    ctx.beginPath();
    ctx.moveTo(w / 2 + Math.cos(a) * 26, 60 + Math.sin(a) * 26);
    ctx.lineTo(w / 2 + Math.cos(a) * 36, 60 + Math.sin(a) * 36);
    ctx.stroke();
  }}
}}

function drawDinosaurBody(ctx, cx, cy, s) {{
  // Dino Body
  ctx.beginPath();
  ctx.ellipse(cx, cy + 20 * s, 90 * s, 70 * s, 0, 0, Math.PI * 2);
  ctx.stroke();

  // Head
  ctx.beginPath();
  ctx.ellipse(cx - 90 * s, cy - 60 * s, 50 * s, 40 * s, -0.2, 0, Math.PI * 2);
  ctx.stroke();

  // Eye & Smile
  ctx.beginPath();
  ctx.arc(cx - 105 * s, cy - 70 * s, 8 * s, 0, Math.PI * 2);
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(cx - 100 * s, cy - 45 * s, 15 * s, 0, Math.PI * 0.8);
  ctx.stroke();

  // Spikes
  for (let i = -3; i <= 3; i++) {{
    const sx = cx + i * 25 * s;
    const sy = cy - 45 * s + Math.abs(i) * 5 * s;
    ctx.beginPath();
    ctx.moveTo(sx - 12 * s, sy);
    ctx.lineTo(sx, sy - 28 * s);
    ctx.lineTo(sx + 12 * s, sy);
    ctx.closePath();
    ctx.stroke();
  }}

  // Tail
  ctx.beginPath();
  ctx.moveTo(cx + 80 * s, cy);
  ctx.quadraticCurveTo(cx + 170 * s, cy - 10 * s, cx + 180 * s, cy - 80 * s);
  ctx.quadraticCurveTo(cx + 140 * s, cy + 40 * s, cx + 70 * s, cy + 50 * s);
  ctx.stroke();

  // Legs
  ctx.strokeRect(cx - 50 * s, cy + 70 * s, 35 * s, 60 * s);
  ctx.strokeRect(cx + 25 * s, cy + 70 * s, 35 * s, 60 * s);
}}

function drawSpaceSubject(ctx, cx, cy, s) {{
  // Rocket Body
  ctx.beginPath();
  ctx.moveTo(cx, cy - 140 * s);
  ctx.quadraticCurveTo(cx - 55 * s, cy - 20 * s, cx - 45 * s, cy + 80 * s);
  ctx.lineTo(cx + 45 * s, cy + 80 * s);
  ctx.quadraticCurveTo(cx + 55 * s, cy - 20 * s, cx, cy - 140 * s);
  ctx.stroke();

  // Porthole Window
  ctx.beginPath();
  ctx.arc(cx, cy - 20 * s, 30 * s, 0, Math.PI * 2);
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(cx, cy - 20 * s, 20 * s, 0, Math.PI * 2);
  ctx.stroke();

  // Fins
  ctx.beginPath();
  ctx.moveTo(cx - 45 * s, cy + 40 * s);
  ctx.lineTo(cx - 95 * s, cy + 95 * s);
  ctx.lineTo(cx - 45 * s, cy + 80 * s);
  ctx.closePath();
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(cx + 45 * s, cy + 40 * s);
  ctx.lineTo(cx + 95 * s, cy + 95 * s);
  ctx.lineTo(cx + 45 * s, cy + 80 * s);
  ctx.closePath();
  ctx.stroke();
}}

function drawOceanSubject(ctx, cx, cy, s) {{
  ctx.beginPath();
  ctx.moveTo(cx - 130 * s, cy + 20 * s);
  ctx.quadraticCurveTo(cx - 50 * s, cy - 90 * s, cx + 70 * s, cy - 30 * s);
  ctx.quadraticCurveTo(cx + 130 * s, cy + 10 * s, cx + 160 * s, cy - 10 * s);
  ctx.lineTo(cx + 150 * s, cy + 40 * s);
  ctx.quadraticCurveTo(cx + 80 * s, cy + 60 * s, cx - 50 * s, cy + 60 * s);
  ctx.closePath();
  ctx.stroke();

  // Fin
  ctx.beginPath();
  ctx.moveTo(cx - 10 * s, cy - 65 * s);
  ctx.quadraticCurveTo(cx + 10 * s, cy - 110 * s, cx + 30 * s, cy - 60 * s);
  ctx.stroke();

  // Eye
  ctx.beginPath();
  ctx.arc(cx - 100 * s, cy - 10 * s, 6 * s, 0, Math.PI * 2);
  ctx.stroke();
}}

function drawSafariSubject(ctx, cx, cy, s) {{
  // Mane
  for (let a = 0; a < Math.PI * 2; a += Math.PI / 6) {{
    const mx = cx + Math.cos(a) * 110 * s;
    const my = cy + Math.sin(a) * 110 * s;
    ctx.beginPath();
    ctx.arc(mx, my, 40 * s, 0, Math.PI * 2);
    ctx.stroke();
  }}

  // Face
  ctx.beginPath();
  ctx.arc(cx, cy, 85 * s, 0, Math.PI * 2);
  ctx.stroke();

  // Eyes
  ctx.beginPath();
  ctx.arc(cx - 32 * s, cy - 15 * s, 14 * s, 0, Math.PI * 2);
  ctx.arc(cx + 32 * s, cy - 15 * s, 14 * s, 0, Math.PI * 2);
  ctx.stroke();
}}

function drawFantasySubject(ctx, cx, cy, s) {{
  ctx.beginPath();
  ctx.ellipse(cx, cy + 20 * s, 70 * s, 90 * s, -0.2, 0, Math.PI * 2);
  ctx.stroke();

  // Horn
  ctx.beginPath();
  ctx.moveTo(cx - 20 * s, cy - 60 * s);
  ctx.lineTo(cx - 10 * s, cy - 160 * s);
  ctx.lineTo(cx + 15 * s, cy - 55 * s);
  ctx.closePath();
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(cx - 25 * s, cy, 12 * s, 0, Math.PI * 2);
  ctx.stroke();
}}

function drawVehicleSubject(ctx, cx, cy, s) {{
  ctx.beginPath();
  ctx.moveTo(cx - 150 * s, cy + 30 * s);
  ctx.quadraticCurveTo(cx - 100 * s, cy - 10 * s, cx - 40 * s, cy - 40 * s);
  ctx.lineTo(cx + 60 * s, cy - 40 * s);
  ctx.quadraticCurveTo(cx + 120 * s, cy - 10 * s, cx + 160 * s, cy + 30 * s);
  ctx.lineTo(cx - 150 * s, cy + 30 * s);
  ctx.stroke();

  // Wheels
  ctx.beginPath();
  ctx.arc(cx - 85 * s, cy + 35 * s, 32 * s, 0, Math.PI * 2);
  ctx.arc(cx + 95 * s, cy + 35 * s, 32 * s, 0, Math.PI * 2);
  ctx.stroke();
}}

function drawIslandSubject(ctx, cx, cy, s) {{
  ctx.beginPath();
  ctx.moveTo(cx - 70 * s, cy + 80 * s);
  ctx.quadraticCurveTo(cx - 40 * s, cy, cx - 60 * s, cy - 80 * s);
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(cx + 80 * s, cy - 50 * s, 45 * s, 0, Math.PI * 2);
  ctx.stroke();
}}

function drawRobotSubject(ctx, cx, cy, s) {{
  ctx.strokeRect(cx - 65 * s, cy - 110 * s, 130 * s, 95 * s);
  ctx.strokeRect(cx - 80 * s, cy, 160 * s, 110 * s);

  ctx.beginPath();
  ctx.arc(cx - 30 * s, cy - 70 * s, 14 * s, 0, Math.PI * 2);
  ctx.arc(cx + 30 * s, cy - 70 * s, 14 * s, 0, Math.PI * 2);
  ctx.stroke();
}}

function drawFoodSubject(ctx, cx, cy, s) {{
  ctx.beginPath();
  ctx.moveTo(cx, cy + 110 * s);
  ctx.lineTo(cx - 100 * s, cy - 90 * s);
  ctx.quadraticCurveTo(cx, cy - 120 * s, cx + 100 * s, cy - 90 * s);
  ctx.closePath();
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(cx, cy - 20 * s, 20 * s, 0, Math.PI * 2);
  ctx.arc(cx - 35 * s, cy + 30 * s, 18 * s, 0, Math.PI * 2);
  ctx.arc(cx + 35 * s, cy + 30 * s, 18 * s, 0, Math.PI * 2);
  ctx.stroke();
}}

function drawMandalaSubject(ctx, cx, cy, s) {{
  const radii = [140 * s, 105 * s, 70 * s, 35 * s];
  radii.forEach(r => {{
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.stroke();
  }});

  for (let a = 0; a < Math.PI * 2; a += Math.PI / 6) {{
    ctx.beginPath();
    ctx.moveTo(cx + Math.cos(a) * 35 * s, cy + Math.sin(a) * 35 * s);
    ctx.lineTo(cx + Math.cos(a) * 140 * s, cy + Math.sin(a) * 140 * s);
    ctx.stroke();
  }}
}}
"""

with open("pages-data.js", "w") as f:
    f.write(js_content)

print("pages-data.js generated successfully")
