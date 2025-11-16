# commands/shop.py
from discord import app_commands, Embed, Interaction
import time

from commands import SHOP_ITEMSa

async def setup(bot, data):
    @bot.tree.command(name="shop", description="View the pirate marketplace.")
    async def shop(interaction: Interaction):
        embed = Embed(title="<a:HUB_pirate_flag:1438231887532265482> **PIRATE BLACK MARKET**", description="*Secret treasures for daring pirates!*", color=0xFFD700)
        for key, item in SHOP_ITEMS.items():
            embed.add_field(name=f"{item['emoji']} {item['name']}", value=f"Price: <:Pirate_Coin:1439446496645746740> **{item['price']}** coins\n*{item['flavor']}*", inline=False)
        embed.set_footer(text="Use /buy <item_id> to make a purchase!")
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="buy", description="Purchase an item from the shop.")
    @app_commands.describe(item="Shop item id (example: mystery_box, double_loot)")
    async def buy(interaction: Interaction, item: str):
        user_id = str(interaction.user.id)
        item_key = item.lower().strip()
        if item_key not in SHOP_ITEMS:
            await interaction.response.send_message("<a:flame_skull1:1438231187633078273> **Item not found in shop, matey!**", ephemeral=True)
            return
        shop_item = SHOP_ITEMS[item_key]
        user = data.get_user(user_id)
        if user["coins"] < shop_item["price"]:
            await interaction.response.send_message("<:skull_token:1439449760124637295> **Ye don't have enough gold for that!**", ephemeral=True)
            return
        # deduct
        user["coins"] -= shop_item["price"]
        # apply effects
        now = time.time()
        if shop_item["type"] == "boost":
            # give boost for 24 hours
            user.setdefault("boosts", {})["double_loot"] = now + 86400
            message = f"<a:curse_gem:1439446670810157116> **Double loot charm activated for 24 hours!**"
        elif shop_item["type"] == "consumable":
            user.setdefault("inventory", {})[shop_item["name"]] = user.get("inventory", {}).get(shop_item["name"], 0) + 1
            message = f"<a:mystry_box_of_pirate:1438237227477110936> **{shop_item['name']} added to your treasure chest!**"
        elif shop_item["type"] == "premium":
            user.setdefault("inventory", {})[shop_item["name"]] = user.get("inventory", {}).get(shop_item["name"], 0) + 1
            message = f"<:legendary:1392576106489708625> **PREMIUM ACQUIRED! {shop_item['name']} is yours!**"
        elif shop_item["type"] == "cosmetic":
            user.setdefault("titles", {})[shop_item["name"]] = True
            message = f"<:PIRATES:1438231801859670107> **Fancy {shop_item['name']} equipped! Look sharp, pirate!**"
        elif shop_item["type"] == "instant":
            user["coins"] += shop_item["reward"]
            message = f"<a:Coins:1438241147540475945> **Instant {shop_item['reward']} coins added to your hoard!**"
        else:
            message = f"<a:dance_of_pirates:1438237492963840150> **You purchased {shop_item['name']}!**"
        await data.save()
        embed = Embed(title="<a:treasure_chest:1439446705354313819> **PURCHASE SUCCESSFUL!**", description=message, color=0x00FF00)
        await interaction.response.send_message(embed=embed)

    return