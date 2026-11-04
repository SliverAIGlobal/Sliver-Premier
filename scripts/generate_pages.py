#!/usr/bin/env python3
"""Generates pages-data.js containing all 120 Vector Coloring Pages across 10 Themed Packs."""

import json

# Define the 10 themed packs and their 12 pages each = 120 total pages
PACKS_CONFIG = [
    {
        "id": "dinosaurs",
        "name": "Dinosaurs & Prehistory",
        "icon": "🦖",
        "pages": [
            ("trex_king", "T-Rex King", "Mighty Tyrannosaurus with sharp teeth and jungle ferns", "junior", "dino"),
            ("triceratops_friend", "Triceratops Friend", "Gentle three-horned herbivore grazing peacefully", "junior", "dino"),
            ("stegosaurus_spikes", "Stegosaurus Spikes", "Armored dinosaur with distinct back plates and tail spikes", "adult", "dino"),
            ("pterodactyl_soar", "Pterodactyl Flight", "Winged reptile soaring above prehistoric cliffs", "junior", "dino"),
            ("brachiosaurus_tall", "Brachiosaurus Reach", "Long-necked giant munching tree canopy leaves", "junior", "dino"),
            ("velociraptor_pack", "Velociraptor Sprint", "Swift agile hunter leaping through prehistoric grass", "adult", "dino"),
            ("ankylosaurus_shield", "Ankylosaurus Club", "Heavy armored tank dinosaur with club tail", "adult", "dino"),
            ("parasaurolophus_crest", "Parasaurolophus Song", "Duck-billed dinosaur with curved head crest", "adult", "dino"),
            ("spinosaurus_river", "Spinosaurus River", "Large sail-backed predator wading in ancient swamps", "adult", "dino"),
            ("baby_dino_egg", "Baby Dino Hatchling", "Cute baby raptor peeking from cracked eggshell", "junior", "dino"),
            ("diplodocus_family", "Diplodocus Herd", "Mother and baby sauropod beside volcanic hills", "junior", "dino"),
            ("fossil_amber_gem", "Fossil Amber Excavation", "Intricate ammonite and dinosaur fossil skeleton", "adult", "dino"),
        ]
    },
    {
        "id": "space",
        "name": "Space & Galaxy",
        "icon": "🚀",
        "pages": [
            ("rocket_explorer", "Rocket Explorer", "Multi-stage spacecraft blasting past constellations", "junior", "space"),
            ("astronaut_dog", "Astronaut Dog", "Courageous puppy in spacesuit floating above Earth", "junior", "space"),
            ("saturn_rings", "Saturn & Rings", "Magnificent gas giant surrounded by swirling icy rings", "adult", "space"),
            ("alien_ufo_visit", "Alien UFO Visit", "Friendly green alien waving from glowing saucer", "junior", "space"),
            ("lunar_rover_quest", "Lunar Rover Trek", "Moon rover rolling over dusty craters", "adult", "space"),
            ("solar_system_orbit", "Solar System Harmony", "Sun, planets, and orbital paths with starry backdrops", "adult", "space"),
            ("space_station_orbit", "Orbital Space Station", "High-tech modular station with solar wing panels", "adult", "space"),
            ("meteor_shower_night", "Cosmic Meteor Shower", "Blazing shooting stars racing across a nebula", "junior", "space"),
            ("black_hole_vortex", "Gravitational Swirl", "Hypnotic accretion disk swirling in deep space", "adult", "space"),
            ("telescope_observatory", "Stargazer Observatory", "Giant dome telescope gazing at distant galaxies", "adult", "space"),
            ("spacewalk_astronaut", "Spacewalk Tether", "Floating astronaut admiring the cosmic vista", "junior", "space"),
            ("mars_colony_dome", "Mars Bio-Dome City", "Futuristic red planet colony under geodesic glass", "adult", "space"),
        ]
    },
    {
        "id": "ocean",
        "name": "Ocean Deep",
        "icon": "🐬",
        "pages": [
            ("playful_dolphin", "Playful Dolphin", "Sleek dolphin leaping over curling ocean waves", "junior", "ocean"),
            ("sea_turtle_glide", "Sea Turtle Glide", "Honu turtle gliding above tropical coral reefs", "junior", "ocean"),
            ("friendly_octopus", "Friendly Octopus", "Whimsical eight-legged friend blowing bubble rings", "junior", "ocean"),
            ("coral_reef_sanctuary", "Coral Reef Sanctuary", "Vibrant anemones, starfish, and clownfish community", "adult", "ocean"),
            ("submarine_quest", "Submarine Quest", "Yellow research vessel illuminating the twilight zone", "junior", "ocean"),
            ("humpback_whale_breach", "Humpback Whale Breach", "Gigantic whale breaching beneath seabirds", "adult", "ocean"),
            ("jellyfish_drift", "Bioluminescent Jellyfish", "Delicate translucent bells and flowing tentacles", "adult", "ocean"),
            ("hammerhead_shark", "Hammerhead Patrol", "Majestic apex swimmer cruising blue currents", "adult", "ocean"),
            ("seahorse_kelp", "Seahorse in Kelp Forest", "Curled-tail seahorse holding golden kelp fronds", "junior", "ocean"),
            ("manta_ray_wings", "Manta Ray Glide", "Graceful oceanic ray gliding over sunken galleon", "adult", "ocean"),
            ("treasure_chest_depths", "Sunken Pirate Treasure", "Gold doubloons and pearls guarded by hermit crabs", "junior", "ocean"),
            ("abyssal_anglerfish", "Abyssal Anglerfish", "Mysterious deep-sea fish with glowing bio-lure", "adult", "ocean"),
        ]
    },
    {
        "id": "safari",
        "name": "Safari & Jungle Animals",
        "icon": "🦁",
        "pages": [
            ("lion_king_savannah", "Lion King Savannah", "Majestic crowned lion resting under acacia tree", "junior", "safari"),
            ("baby_elephant_splash", "Baby Elephant Splash", "Playful young calf spraying water on riverbank", "junior", "safari"),
            ("tall_giraffe_canopy", "Tall Giraffe Canopy", "Spotted giraffe reaching highest sweet leaves", "junior", "safari"),
            ("playful_monkey_vines", "Playful Monkey Vines", "Agile chimp swinging through leafy jungle canopy", "junior", "safari"),
            ("panda_bamboo_grove", "Panda Bamboo Grove", "Plump panda munching fresh tender bamboo stalks", "junior", "safari"),
            ("zebra_stripes_wild", "Zebra Crossing", "Dazzling optical stripes on open savannah plains", "adult", "safari"),
            ("rhino_armored_graze", "Rhino Stronghold", "Two-horned rhino walking alongside birds", "adult", "safari"),
            ("cheetah_sprint", "Cheetah Speedster", "Fastest land predator resting after high sprint", "adult", "safari"),
            ("hippo_river_pool", "Hippo Mud Lagoon", "Chubby river hippo smiling among water lilies", "junior", "safari"),
            ("tiger_bengal_stride", "Bengal Tiger Stride", "Striped apex king stalking through lush ferns", "adult", "safari"),
            ("toucan_tropical_perch", "Toucan Rainbow Beak", "Vibrant bill bird perched upon jungle branch", "junior", "safari"),
            ("koala_eucalyptus_nap", "Koala Eucalyptus Nap", "Cuddly marsupial dozing in tree crook", "junior", "safari"),
        ]
    },
    {
        "id": "fairytales",
        "name": "Fairytales & Fantasy",
        "icon": "🦄",
        "pages": [
            ("enchanted_unicorn", "Enchanted Unicorn", "Horned steed prancing through flower meadows", "junior", "fantasy"),
            ("fire_dragon_roost", "Fire Dragon Roost", "Grand scaled wyrm guarding mountain crystals", "adult", "fantasy"),
            ("magic_castle_turrets", "Magic Kingdom Castle", "Fairytale fortress with banners, spires, and moats", "adult", "fantasy"),
            ("wizard_potion_lab", "Wizard Potion Workshop", "Bubbling cauldrons, spell books, and crystal orbs", "adult", "fantasy"),
            ("pegasus_cloud_flight", "Pegasus Winged Flight", "Stallion soaring across fluffy sunset clouds", "junior", "fantasy"),
            ("mermaid_lagoon", "Mermaid Pearl Lagoon", "Ocean maiden combing hair atop glistening rocks", "adult", "fantasy"),
            ("fairy_mushroom_village", "Fairy Mushroom Village", "Tiny cobblestone cottage inside spotted toadstool", "junior", "fantasy"),
            ("phoenix_rebirth", "Phoenix Sun Firebird", "Radiant feather wings rising from celestial embers", "adult", "fantasy"),
            ("gnome_forest_forge", "Woodland Gnome Haven", "Bearded tinker crafting lantern gear in hollow oak", "adult", "fantasy"),
            ("crystal_treasure_cave", "Crystal Cavern Grotto", "Glittering amethyst geodes and ancient runes", "adult", "fantasy"),
            ("flying_carpet_bazaar", "Magic Carpet Journey", "Carpet sailing past minarets and starlight", "junior", "fantasy"),
            ("princess_flower_garden", "Princess Royal Arbor", "Flowing royal gown among blossoming roses", "junior", "fantasy"),
        ]
    },
    {
        "id": "vehicles",
        "name": "Vehicles & Speed",
        "icon": "🏎️",
        "pages": [
            ("super_race_car", "Super Race Car", "Aerodynamic race car speeding across finish line", "junior", "vehicles"),
            ("fire_engine_hero", "Fire Engine Hero", "Ladder truck with sirens, hoses, and flashing lights", "junior", "vehicles"),
            ("police_chopper_air", "Police Helicopter", "Rescue chopper circling city skyline", "junior", "vehicles"),
            ("monster_truck_jam", "Monster Truck Giant", "Giant off-road wheels crushing obstacle ramps", "junior", "vehicles"),
            ("jet_aircraft_sonic", "Supersonic Fighter Jet", "Streamlined delta-wing aircraft breaking cloud barrier", "adult", "vehicles"),
            ("digger_excavator", "Construction Excavator", "Heavy excavator shovel scooping rocky quarry", "junior", "vehicles"),
            ("steam_train_express", "Steam Locomotive", "Classic locomotive puffing billows across railway bridge", "adult", "vehicles"),
            ("motorcycle_cruiser", "Vintage Cruiser Bike", "Chrome engine cylinders and touring road wheels", "adult", "vehicles"),
            ("tugboat_harbor_guide", "Sturdy Harbor Tugboat", "Charming boat guiding ocean liner into port", "junior", "vehicles"),
            ("sailboat_regatta", "Twin-Sail Regatta", "Catamaran slicing white waves in coastal breeze", "adult", "vehicles"),
            ("tractor_farm_harvest", "Farmstead Tractor", "Field tractor rolling through golden wheat sheaves", "junior", "vehicles"),
            ("hot_air_balloon_float", "Hot Air Balloon Float", "Striped balloon drifting above patchwork valleys", "junior", "vehicles"),
        ]
    },
    {
        "id": "island",
        "name": "808 Island Paradise",
        "icon": "🌺",
        "pages": [
            ("aloha_honu_turtle", "Aloha Honu Turtle", "Sacred Hawaiian turtle resting beside plumeria flowers", "junior", "island"),
            ("palm_tree_sunset_surf", "Waikiki Sunset Palms", "Silhouetted palms framing diamond surf breakers", "junior", "island"),
            ("hawaiian_hibiscus_bloom", "Yellow Maʻo Hau Hele", "State hibiscus with graceful stamen and petals", "junior", "island"),
            ("outrigger_canoe_voyage", "Waʻa Outrigger Canoe", "Polynesian sailing canoe navigating Pacific swells", "adult", "island"),
            ("kilauea_volcano_glow", "Kilauea Volcano Peak", "Lava fountain forming obsidian island shores", "adult", "island"),
            ("ukulele_tiki_hut", "Ukulele & Tiki Hut", "Four-string wooden ukulele resting near beach lanai", "junior", "island"),
            ("humpback_maui_channel", "Maui Whale Sanctuary", "Mother and calf whale playing off Lahaina roadstead", "adult", "island"),
            ("hula_dancer_lei", "Graceful Hula Dancer", "Traditional dancer adorned in floral lei and ti leaves", "adult", "island"),
            ("pineapple_plantation", "Sweet Crown Pineapple", "Tropical golden fruit with sharp crown leaves", "junior", "island"),
            ("tropical_reef_humuhumu", "Humuhumunukunukuapuaʻa", "Iconic wedge-tail triggerfish in crystal tidepools", "adult", "island"),
            ("waterfall_valley_lush", "Secret Valley Cascade", "Twin waterfalls plunging into fern-ringed pool", "adult", "island"),
            ("shave_ice_rainbow_delight", "Rainbow Shave Ice", "Snow cone with tropical syrups, mochi, and azuki", "junior", "island"),
        ]
    },
    {
        "id": "robots",
        "name": "Robots & Future",
        "icon": "🤖",
        "pages": [
            ("helper_bot_9000", "Helper Bot 9000", "Friendly home assistant robot holding duster and tea", "junior", "robot"),
            ("robot_dog_companion", "Cyber K-9 Puppy", "Mechanical dog with wagging antenna tail", "junior", "robot"),
            ("space_mech_titan", "Space Mech Titan", "Giant robotic exosuit protecting orbital outpost", "adult", "robot"),
            ("eco_bot_planter", "Eco-Bot Gardener", "Solar robot tender planting acorns and green saplings", "junior", "robot"),
            ("flying_drone_scout", "Quad-Rotor Drone", "High-speed surveillance drone hovering over futuristic city", "junior", "robot"),
            ("cyber_cat_prowl", "Bionic Cyber Cat", "Sleek robotic feline perched on neon skyscraper ledge", "adult", "robot"),
            ("android_inventor_bench", "Android Laboratory", "Scientist bot calibrating photon lasers and circuit boards", "adult", "robot"),
            ("nanobot_circuit_matrix", "Microchip Highway", "Intricate circuit traces, logic gates, and glowing micro-cores", "adult", "robot"),
            ("solar_crawler_rover", "Solar Desert Crawler", "Multi-wheeled robotic rover surveying geothermal plains", "adult", "robot"),
            ("deep_sea_submersible_bot", "Aquatic Drone Sub", "Torpedo-shaped exploration sub with robotic arms", "adult", "robot"),
            ("retro_clockwork_automaton", "Clockwork Brass Bot", "Vintage steampunk robot with winding key and dials", "adult", "robot"),
            ("hover_delivery_bot", "Hover Courier Express", "Anti-gravity courier bot zipping across skyways", "junior", "robot"),
        ]
    },
    {
        "id": "sweets",
        "name": "Sweets & Yummy Foods",
        "icon": "🍕",
        "pages": [
            ("happy_pizza_slice", "Happy Pizza Slice", "Melted cheese slice grinning with pepperoni eyes", "junior", "food"),
            ("ice_cream_tower_triple", "Triple Scoop Sundae", "Waffle cone piled with strawberry, mint, and chocolate", "junior", "food"),
            ("sprinkle_donut_glaze", "Giant Frosted Donut", "Rich glaze with sprinkles and playful bite mark", "junior", "food"),
            ("boba_tea_cup_kawaii", "Kawaii Boba Tea Cup", "Smile cup filled with sweet milk tea and chewy pearls", "junior", "food"),
            ("cupcake_stack_delight", "Birthday Cupcake Swirl", "Fluffy swirl icing with sprinkles and birthday candle", "junior", "food"),
            ("crispy_taco_fiesta", "Crunchy Taco Fiesta", "Folded tortilla loaded with lettuce, cheese, and salsa", "junior", "food"),
            ("pancake_butter_stack", "Syrup Pancake Tower", "Golden pancake stack with melting butter square", "junior", "food"),
            ("sushi_roll_platter", "Nigiri & Maki Platter", "Artful wooden board of salmon nigiri and avocado rolls", "adult", "food"),
            ("fruit_smoothie_bowl", "Berry Acai Smoothie Bowl", "Arranged kiwi slices, blueberries, and chia seeds", "adult", "food"),
            ("gingerbread_candy_house", "Gingerbread Fantasy House", "Candy cane pillars, gumdrop roof, and frosting door", "adult", "food"),
            ("chocolate_fountain_buffet", "Cascade Chocolate Fountain", "Flowing chocolate dips for strawberries and marshmallows", "adult", "food"),
            ("candy_store_jars", "Vintage Sweet Shoppe", "Glass jars of lollipops, jelly beans, and ribbon candy", "adult", "food"),
        ]
    },
    {
        "id": "mandalas",
        "name": "Mandalas & Patterns",
        "icon": "🎨",
        "pages": [
            ("starburst_wheel", "Starburst Sun Wheel", "Bold radial symmetry with alternating solar flares", "junior", "pattern"),
            ("floral_mosaic_mandala", "Floral Mosaic Rose", "Concentric botanical petals with intricate lace border", "adult", "pattern"),
            ("cosmic_swirl_galaxy", "Cosmic Spiral Vortex", "Logarithmic spiral of stars, crescents, and sacred geometry", "adult", "pattern"),
            ("diamond_lattice_geometric", "Diamond Optical Lattice", "Tessellated harlequin pattern with 3D illusions", "adult", "pattern"),
            ("ocean_waves_crest_mandala", "Hokusai Wave Ring", "Circular repeating tidal waves and sea spray foam", "adult", "pattern"),
            ("celtic_knot_shield", "Celtic Knotwork Shield", "Intertwined continuous knot bands of eternal strength", "adult", "pattern"),
            ("kaleidoscope_butterflies", "Kaleidoscope Butterflies", "Eight-fold symmetrical butterfly ring with floral center", "adult", "pattern"),
            ("mandala_lotus_blossom", "Sacred Lotus Bloom", "Peaceful serene waterlily mandala with petal layers", "junior", "pattern"),
            ("mandala_sun_and_moon", "Sun & Moon Union", "Harmonious balance of daytime rays and midnight stars", "junior", "pattern"),
            ("hexagonal_honeycomb_hive", "Geometric Honeycomb Lattice", "Busy geometric hive pattern with hexagon cells", "junior", "pattern"),
            ("tribal_zigzag_blanket", "Navajo Geometric Tapestry", "Stepped pyramids, chevron zigzags, and arrowheads", "junior", "pattern"),
            ("arabesque_tile_palace", "Alhambra Arabesque Tile", "Interlocking Moorish star tile geometry", "adult", "pattern"),
        ]
    }
]

# Procedural High-Contrast Vector SVG Generator for each page
def generate_page_svg(page_id, title, theme, difficulty):
    is_adult = (difficulty == "adult")
    stroke_w = 4 if is_adult else 8
    fine_w = 2 if is_adult else 5

    # Base SVG with crisp coloring lines
    elements = []
    # Outer frame
    elements.append(f'<rect x="20" y="20" width="760" height="760" rx="16" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>')

    if theme == "dino":
        elements.append(f'''
        <!-- Dino Body Archetype: {page_id} -->
        <path d="M180,600 C150,420 220,280 380,240 C520,200 640,240 680,340 C700,390 660,450 580,440 C520,430 480,480 460,560 L500,680 L440,680 L420,580 L320,580 L300,680 L240,680 L260,570 C220,590 190,620 180,600 Z" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Dino Eye & Smile -->
        <circle cx="560" cy="310" r="14" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="564" cy="308" r="5" fill="#000000"/>
        <path d="M590,360 Q630,370 650,350" fill="none" stroke="#000000" stroke-width="{stroke_w}" stroke-linecap="round"/>
        <!-- Prehistoric Fern Leaves / Ground -->
        <path d="M60,720 Q240,660 400,720 T740,700" fill="none" stroke="#000000" stroke-width="{stroke_w}"/>
        <polygon points="340,230 380,160 410,235" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <polygon points="430,235 470,155 500,245" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <polygon points="260,260 290,190 320,250" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        ''')
        if is_adult:
            # Detailed scales & texture
            for y in range(350, 520, 45):
                elements.append(f'<path d="M300,{y} Q330,{y-15} 360,{y} Q390,{y-15} 420,{y}" fill="none" stroke="#000000" stroke-width="{fine_w}"/>')
            elements.append(f'<polygon points="680,680 720,550 760,680" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>')

    elif theme == "space":
        elements.append(f'''
        <!-- Cosmic / Space Archetype: {page_id} -->
        <circle cx="400" cy="400" r="180" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <ellipse cx="400" cy="400" rx="320" ry="70" fill="none" stroke="#000000" stroke-width="{stroke_w}" transform="rotate(-20 400 400)"/>
        <!-- Rocket / Probe -->
        <path d="M220,240 C280,180 340,160 380,160 C380,200 360,260 300,320 Z" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="310" cy="230" r="22" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <polygon points="230,280 180,310 210,250" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Stars & Constellations -->
        <polygon points="120,120 126,140 146,140 130,152 136,172 120,160 104,172 110,152 94,140 114,140" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>
        <polygon points="680,150 686,170 706,170 690,182 696,202 680,190 664,202 670,182 654,170 674,170" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>
        <polygon points="650,620 656,640 676,640 660,652 666,672 650,660 634,672 640,652 624,640 644,640" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>
        ''')
        if is_adult:
            elements.append(f'<path d="M100,500 C250,550 350,650 550,600 C650,580 700,660 750,700" fill="none" stroke="#000000" stroke-width="{fine_w}"/>')

    elif theme == "ocean":
        elements.append(f'''
        <!-- Ocean Deep Archetype: {page_id} -->
        <!-- Sea Turtle / Dolphin Form -->
        <ellipse cx="400" cy="420" rx="160" ry="110" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <ellipse cx="580" cy="400" rx="45" ry="32" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="595" cy="392" r="6" fill="#000000"/>
        <!-- Flippers -->
        <path d="M460,340 C520,200 440,160 380,260 Z" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <path d="M460,500 C520,640 440,680 380,580 Z" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <path d="M260,380 C200,320 180,360 220,410 Z" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <path d="M260,460 C200,520 180,480 220,430 Z" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Waves & Bubbles -->
        <circle cx="650" cy="300" r="18" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>
        <circle cx="680" cy="240" r="12" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>
        <circle cx="630" cy="200" r="8" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>
        <path d="M60,180 C200,120 320,220 500,160 C620,120 700,190 760,160" fill="none" stroke="#000000" stroke-width="{stroke_w}"/>
        ''')
        if is_adult:
            # Turtle shell scutes
            elements.append(f'<polygon points="400,350 440,390 440,450 400,490 360,450 360,390" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>')
            elements.append(f'<polygon points="320,380 350,400 350,440 320,460 290,440 290,400" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>')
            elements.append(f'<polygon points="480,380 510,400 510,440 480,460 450,440 450,400" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>')

    elif theme == "safari":
        elements.append(f'''
        <!-- Safari & Jungle Archetype: {page_id} -->
        <circle cx="400" cy="380" r="140" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Big Ears -->
        <circle cx="280" cy="280" r="45" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="520" cy="280" r="45" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Face Features -->
        <circle cx="350" cy="360" r="12" fill="#000000"/>
        <circle cx="450" cy="360" r="12" fill="#000000"/>
        <ellipse cx="400" cy="420" rx="35" ry="24" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <ellipse cx="400" cy="410" rx="15" ry="10" fill="#000000"/>
        <path d="M400,420 L400,440 M380,440 Q400,455 420,440" fill="none" stroke="#000000" stroke-width="{stroke_w}" stroke-linecap="round"/>
        <!-- Jungle Foliage Background -->
        <path d="M120,680 C180,520 280,560 340,680 Z" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <path d="M680,680 C620,520 520,560 460,680 Z" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        ''')
        if is_adult:
            elements.append(f'''
            <path d="M400,200 C320,240 240,320 220,420 C200,520 280,620 400,640 C520,620 600,520 580,420 C560,320 480,240 400,200" fill="none" stroke="#000000" stroke-width="{fine_w}"/>
            ''')

    elif theme == "fantasy":
        elements.append(f'''
        <!-- Fantasy & Fairytale Archetype: {page_id} -->
        <!-- Castle Towers / Dragon Wings -->
        <polygon points="400,100 340,240 460,240" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <rect x="350" y="240" width="100" height="340" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Left & Right Flank Towers -->
        <polygon points="220,220 180,320 260,320" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <rect x="190" y="320" width="60" height="260" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <polygon points="580,220 540,320 620,320" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <rect x="550" y="320" width="60" height="260" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Castle Gate -->
        <path d="M370,580 C370,500 430,500 430,580 Z" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Magic Star / Crescent Moon -->
        <path d="M680,80 A35,35 0 1,1 640,140 A38,38 0 0,0 680,80 Z" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        ''')
        if is_adult:
            elements.append(f'''
            <line x1="350" y1="340" x2="450" y2="340" stroke="#000000" stroke-width="{fine_w}"/>
            <line x1="350" y1="420" x2="450" y2="420" stroke="#000000" stroke-width="{fine_w}"/>
            <line x1="350" y1="500" x2="450" y2="500" stroke="#000000" stroke-width="{fine_w}"/>
            ''')

    elif theme == "vehicles":
        elements.append(f'''
        <!-- Vehicles & Speed Archetype: {page_id} -->
        <path d="M160,520 L240,360 L540,360 L660,520 Z" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <rect x="140" y="500" width="540" height="80" rx="20" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Wheels -->
        <circle cx="260" cy="580" r="50" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="260" cy="580" r="24" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="560" cy="580" r="50" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="560" cy="580" r="24" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Windows -->
        <polygon points="260,500 300,380 430,380 430,500" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>
        <polygon points="450,500 450,380 530,380 580,500" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>
        <!-- Speed lines / Road -->
        <line x1="60" y1="670" x2="740" y2="670" stroke="#000000" stroke-width="{stroke_w}"/>
        ''')
        if is_adult:
            elements.append(f'<line x1="60" y1="320" x2="180" y2="320" stroke="#000000" stroke-width="{fine_w}" stroke-dasharray="10,10"/>')
            elements.append(f'<line x1="90" y1="350" x2="200" y2="350" stroke="#000000" stroke-width="{fine_w}" stroke-dasharray="10,10"/>')

    elif theme == "island":
        elements.append(f'''
        <!-- 808 Island Paradise Archetype: {page_id} -->
        <!-- Diamond Head / Volcano silhouette -->
        <polygon points="120,580 340,420 540,460 720,580" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Palm Tree -->
        <path d="M260,620 Q220,400 320,280" fill="none" stroke="#000000" stroke-width="{stroke_w+4}" stroke-linecap="round"/>
        <path d="M320,280 C220,220 120,280 80,340" fill="none" stroke="#000000" stroke-width="{stroke_w}" stroke-linecap="round"/>
        <path d="M320,280 C360,180 460,200 500,260" fill="none" stroke="#000000" stroke-width="{stroke_w}" stroke-linecap="round"/>
        <path d="M320,280 C260,160 380,140 400,220" fill="none" stroke="#000000" stroke-width="{stroke_w}" stroke-linecap="round"/>
        <!-- Ocean Surf Shoreline -->
        <path d="M60,620 C200,580 360,640 520,600 C640,570 700,630 760,610" fill="none" stroke="#000000" stroke-width="{stroke_w}"/>
        <path d="M60,680 C220,640 380,700 540,660 C660,630 720,690 760,670" fill="none" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Hibiscus Motif -->
        <circle cx="620" cy="240" r="30" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="620" cy="240" r="12" fill="#000000"/>
        ''')
        if is_adult:
            for angle in [0, 72, 144, 216, 288]:
                elements.append(f'<ellipse cx="620" cy="240" rx="22" ry="50" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}" transform="rotate({angle} 620 240)"/>')

    elif theme == "robot":
        elements.append(f'''
        <!-- Robots & Future Archetype: {page_id} -->
        <rect x="260" y="220" width="280" height="240" rx="30" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Antenna -->
        <line x1="400" y1="120" x2="400" y2="220" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="400" cy="110" r="20" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Eyes / Sensor screen -->
        <rect x="300" y="270" width="200" height="80" rx="14" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="350" cy="310" r="22" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="350" cy="310" r="10" fill="#000000"/>
        <circle cx="450" cy="310" r="22" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="450" cy="310" r="10" fill="#000000"/>
        <!-- Speaker mouth grill -->
        <rect x="340" y="385" width="120" height="30" rx="8" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <line x1="370" y1="385" x2="370" y2="415" stroke="#000000" stroke-width="{fine_w}"/>
        <line x1="400" y1="385" x2="400" y2="415" stroke="#000000" stroke-width="{fine_w}"/>
        <line x1="430" y1="385" x2="430" y2="415" stroke="#000000" stroke-width="{fine_w}"/>
        <!-- Robot Torso -->
        <rect x="280" y="480" width="240" height="200" rx="20" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="400" cy="570" r="35" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        ''')
        if is_adult:
            # Circuit traces
            elements.append(f'<path d="M120,300 L200,300 L200,450 L260,450" fill="none" stroke="#000000" stroke-width="{fine_w}"/>')
            elements.append(f'<circle cx="120" cy="300" r="6" fill="#000000"/>')
            elements.append(f'<path d="M680,300 L600,300 L600,450 L540,450" fill="none" stroke="#000000" stroke-width="{fine_w}"/>')
            elements.append(f'<circle cx="680" cy="300" r="6" fill="#000000"/>')

    elif theme == "food":
        elements.append(f'''
        <!-- Sweets & Food Archetype: {page_id} -->
        <!-- Big Sundae / Cupcake / Pizza slice -->
        <polygon points="400,160 220,580 580,580" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <path d="M200,580 Q400,640 600,580" fill="none" stroke="#000000" stroke-width="{stroke_w+2}"/>
        <!-- Pepperoni / Fruit toppings -->
        <circle cx="400" cy="300" r="32" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="330" cy="420" r="30" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="470" cy="420" r="30" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="400" cy="500" r="34" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Smiling Eyes & Face -->
        <circle cx="370" cy="360" r="6" fill="#000000"/>
        <circle cx="430" cy="360" r="6" fill="#000000"/>
        <path d="M385,380 Q400,395 415,380" fill="none" stroke="#000000" stroke-width="{stroke_w}" stroke-linecap="round"/>
        ''')
        if is_adult:
            # Cheese drizzle & herbs
            elements.append(f'<ellipse cx="360" cy="480" rx="15" ry="6" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>')
            elements.append(f'<ellipse cx="440" cy="480" rx="15" ry="6" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>')

    elif theme == "pattern":
        elements.append(f'''
        <!-- Mandala & Pattern Archetype: {page_id} -->
        <circle cx="400" cy="400" r="330" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="400" cy="400" r="250" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="400" cy="400" r="170" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <circle cx="400" cy="400" r="90" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <!-- Radial 8-point geometric stars -->
        <polygon points="400,150 440,230 400,310 360,230" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <polygon points="400,650 440,570 400,490 360,570" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <polygon points="150,400 230,440 310,400 230,360" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        <polygon points="650,400 570,440 490,400 570,360" fill="#ffffff" stroke="#000000" stroke-width="{stroke_w}"/>
        ''')
        if is_adult:
            for angle in [45, 135, 225, 315]:
                elements.append(f'''
                <g transform="rotate({angle} 400 400)">
                  <polygon points="400,150 430,220 400,290 370,220" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>
                  <circle cx="400" cy="220" r="14" fill="#ffffff" stroke="#000000" stroke-width="{fine_w}"/>
                </g>''')

    body = "\n".join(elements)
    return f'<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">\n{body}\n</svg>'

# Compile all 120 pages
ALL_PAGES = []
for pack in PACKS_CONFIG:
    for page_id, title, desc, diff, theme in pack["pages"]:
        svg_code = generate_page_svg(page_id, title, theme, diff)
        ALL_PAGES.append({
            "id": page_id,
            "title": title,
            "packId": pack["id"],
            "packName": pack["name"],
            "packIcon": pack["icon"],
            "description": desc,
            "difficulty": diff,
            "theme": theme,
            "svg": svg_code
        })

print(f"Total Pages Generated: {len(ALL_PAGES)}")
assert len(ALL_PAGES) == 120, f"Expected 120 pages, got {len(ALL_PAGES)}"

output_js = f"""// 120 Vector Coloring Pages across 10 Themed Packs for Version 2 ULTRA
// Zero external files - 100% self-contained high-contrast vector outlines

window.COLORING_PACKS = {json.dumps(PACKS_CONFIG, indent=2)};
window.COLORING_PAGES = {json.dumps(ALL_PAGES, indent=2)};
"""

with open('pages-data.js', 'w') as f:
    f.write(output_js)

print("Saved pages-data.js successfully.")
