# utils.py
import random
import discord

# intents: allow what you need
INTENTS = discord.Intents.default()
INTENTS.message_content = False
INTENTS.members = True
INTENTS.reactions = True

# Rarity definitions (same chances as your original)
RARITIES = {
    "Common": {"chance": 55, "color": 0x808080, "emoji": "<:coin2_silver_piece:1439446611154571407>"},
    "Uncommon": {"chance": 25, "color": 0x00ff00, "emoji": "<:Pirate_Coin:1439446496645746740>"},
    "Rare": {"chance": 12, "color": 0x0080ff, "emoji": "<:coin_Ancient:1439446547866845224>"},
    "Epic": {"chance": 5, "color": 0x800080, "emoji": "<:Gold_Bars:1439446648756506656>"},
    "Legendary": {"chance": 2.5, "color": 0xffa500, "emoji": "<a:curse_gem:1439446670810157116>"},
    "Mythic": {"chance": 0.5, "color": 0xff0000, "emoji": "<a:flame_skull1:1438231187633078273>"},
}

# LOOT / SHOP / TITLES: For brevity, minimal examples included.
# You may extend these dictionaries. Keep names identical to what you used previously.
LOOT_ITEMS = {
    "Common": [
        {"name": "Silver Doubloon", "emoji": "<:coin2_silver_piece:1439446611154571407>", "value": 15, "type": "currency", "flavor": "A basic pirate's pay!"},
        {"name": "Rusty Compass", "emoji": "<:pirate_reviewer:1438237310708617386>", "value": 20, "type": "item", "flavor": "Points... somewhere?"}
    ],
    "Uncommon": [
        {"name": "Pirate Gold", "emoji": "<:Pirate_Coin:1439446496645746740>", "value": 35, "type": "currency", "flavor": "Shiny pieces of eight!"}
    ],
    "Rare": [
        {"name": "Ancient Doubloon", "emoji": "<:coin_Ancient:1439446547866845224>", "value": 65, "type": "currency", "flavor": "From a lost civilization!"}
    ],
    "Epic": [
        {"name": "Gold Bar Stack", "emoji": "<:Gold_Bars:1439446648756506656>", "value": 120, "type": "currency", "flavor": "A king's ransom!"}
    ],
    "Legendary": [
        {"name": "Cursed Gem", "emoji": "<a:curse_gem:1439446670810157116>", "value": 300, "type": "item", "flavor": "Pulses with dark energy!"}
    ],
    "Mythic": [
        {"name": "Flaming Skull Artifact", "emoji": "<a:flame_skull1:1438231187633078273>", "value": 800, "type": "item", "flavor": "Burns with eternal fire!"}
    ]
}

SHOP_ITEMS = {
    "mystery_box": {"name": "Mystery Treasure Chest", "price": 100, "emoji": "<a:mystery_box:1439446758911381545>", "type": "consumable", "flavor": "What wonders inside?"},
    "double_loot": {"name": "Double Loot Charm", "price": 300, "emoji": "<a:curse_gem:1439446670810157116>", "type": "boost", "flavor": "Double the treasure!"}
}

TITLES = {
    "Deck Swabber": {"requirement": 0, "emoji": "<:rookie:1392576056971493619>"},
    "Sailor": {"requirement": 500, "emoji": "<:pirates:1438231834088701982>"},
    "Gunner": {"requirement": 1500, "emoji": "💥"},
    "First Mate": {"requirement": 4000, "emoji": "<:elite:1392576075090890924>"},
}

# Flatten item-name -> rarity mapping for convenience
ITEM_TO_RARITY = {}
for r, items in LOOT_ITEMS.items():
    for it in items:
        ITEM_TO_RARITY[it["name"]] = r

def get_rarity():
    roll = random.random() * 100
    cumulative = 0
    for rarity, data in RARITIES.items():
        cumulative += data["chance"]
        if roll <= cumulative:
            return rarity
    return "Common"

def get_user_title(coins: int) -> str:
    # find the highest title whose requirement <= coins
    possible = sorted(TITLES.items(), key=lambda kv: kv[1]["requirement"], reverse=True)
    for title, data in possible:
        if coins >= data["requirement"]:
            return title
    return "Deck Swabber"
