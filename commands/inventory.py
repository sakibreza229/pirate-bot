# commands/inventory.py
from discord import app_commands, Embed, Interaction
from utils import ITEM_TO_RARITY, RARITIES, LOOT_ITEMS

async def setup(bot, data):
    @bot.tree.command(name="inventory", description="Display your pirate treasure collection.")
    async def inventory(interaction: Interaction):
        user_id = str(interaction.user.id)
        user = data.get_user(user_id)
        inv = user.get("inventory", {})
        
        embed = Embed(
            title=f"<a:treasure_chest:1439446705354313819> **{interaction.user.display_name.upper()}'S TREASURE VAULT**",
            color=0x8B4513
        )
        
        if not inv:
            embed.description = "**<:skull_token:1439449760124637295> YARR! YER TREASURE CHEST BE EMPTY!**\nUse `/loot` to begin yer plunderin' journey!"
            await interaction.response.send_message(embed=embed)
            return

        # PIRATE EXPRESS SUMMARY
        total_items = sum(inv.values())
        total_value = 0
        legendary_count = 0
        
        for item_name, quantity in inv.items():
            # Calculate item value
            for rarity_items in LOOT_ITEMS.values():
                for loot in rarity_items:
                    if loot["name"] == item_name:
                        total_value += loot["value"] * quantity
                        if loot["value"] >= 200:  # Legendary threshold
                            legendary_count += quantity
                        break

        # PIRATE EXPRESS HEADER
        embed.add_field(
            name="<a:HUB_pirate_flag:1438231887532265482> **PIRATE EXPRESS SUMMARY**",
            value=(
                f"<a:Coins:1438241147540475945> **Total Value:** {total_value:,} gold\n"
                f"<a:mystry_box_of_pirate:1438237227477110936> **Items Collected:** {total_items}\n"
                f"<:legendary:1392576106489708625> **Legendary Finds:** {legendary_count}\n"
                f"<:pirate_reviewer:1438237310708617386> **Unique Treasures:** {len(inv)}"
            ),
            inline=False
        )

        # ANCIENT TREASURE GALLERY - Group by rarity with PIRATE STYLING
        grouped = {}
        for name, qty in inv.items():
            rarity = ITEM_TO_RARITY.get(name, "Common")
            grouped.setdefault(rarity, []).append((name, qty))

        # MYTHIC TREASURES - GODLY ITEMS
        if grouped.get("Mythic"):
            mythic_text = []
            for name, qty in grouped["Mythic"]:
                item_emoji = "<a:flame_skull1:1438231187633078273>"
                for loot in LOOT_ITEMS["Mythic"]:
                    if loot["name"] == name:
                        item_emoji = loot["emoji"]
                        break
                mythic_text.append(f"{item_emoji} **{name}** ×**{qty}**")
            
            embed.add_field(
                name="<:master:1392576120569856001> **MYTHIC ARTIFACTS**",
                value="\n".join(mythic_text),
                inline=False
            )

        # LEGENDARY RELICS - ANCIENT POWER
        if grouped.get("Legendary"):
            legendary_text = []
            for name, qty in grouped["Legendary"]:
                item_emoji = "<:Black_Pearl:1439449434885980240>"
                for loot in LOOT_ITEMS["Legendary"]:
                    if loot["name"] == name:
                        item_emoji = loot["emoji"]
                        break
                legendary_text.append(f"{item_emoji} **{name}** ×**{qty}**")
            
            embed.add_field(
                name="<:legendary:1392576106489708625> **LEGENDARY RELICS**",
                value="\n".join(legendary_text),
                inline=True
            )

        # EPIC BOUNTY - CAPTAIN'S PRIZES
        if grouped.get("Epic"):
            epic_text = []
            for name, qty in grouped["Epic"]:
                item_emoji = "<:Gold_Bars:1439446648756506656>"
                for loot in LOOT_ITEMS["Epic"]:
                    if loot["name"] == name:
                        item_emoji = loot["emoji"]
                        break
                epic_text.append(f"{item_emoji} **{name}** ×**{qty}**")
            
            embed.add_field(
                name="<:veteran:1392576091608055958> **EPIC BOUNTY**",
                value="\n".join(epic_text),
                inline=True
            )

        # RARE FINDS - FIRST MATE'S COLLECTION
        if grouped.get("Rare"):
            rare_text = []
            for name, qty in grouped["Rare"]:
                item_emoji = "<:coin_Ancient:1439446547866845224>"
                for loot in LOOT_ITEMS["Rare"]:
                    if loot["name"] == name:
                        item_emoji = loot["emoji"]
                        break
                rare_text.append(f"{item_emoji} **{name}** ×**{qty}**")
            
            embed.add_field(
                name="<:elite:1392576075090890924> **RARE FINDS**",
                value="\n".join(rare_text),
                inline=True
            )

        # UNCOMMON GOODS - CREW'S SHARE
        if grouped.get("Uncommon"):
            uncommon_text = []
            for name, qty in grouped["Uncommon"]:
                item_emoji = "<:Pirate_Coin:1439446496645746740>"
                for loot in LOOT_ITEMS["Uncommon"]:
                    if loot["name"] == name:
                        item_emoji = loot["emoji"]
                        break
                uncommon_text.append(f"{item_emoji} **{name}** ×**{qty}**")
            
            embed.add_field(
                name="<:rookie:1392576056971493619> **UNCOMMON GOODS**",
                value="\n".join(uncommon_text),
                inline=True
            )

        # COMMON STASH - DECK SWABBER'S ITEMS
        if grouped.get("Common"):
            common_text = []
            for name, qty in grouped["Common"]:
                item_emoji = "<:coin2_silver_piece:1439446611154571407>"
                for loot in LOOT_ITEMS["Common"]:
                    if loot["name"] == name:
                        item_emoji = loot["emoji"]
                        break
                common_text.append(f"{item_emoji} **{name}** ×**{qty}**")
            
            embed.add_field(
                name="<:pro:1392576041876324502> **COMMON STASH**",
                value="\n".join(common_text),
                inline=True
            )

        # TREASURE VAULT STATS
        vault_stats = []
        if legendary_count >= 5:
            vault_stats.append("<:Jack_Sparrow:1438231857857695834> **Legendary Collector**")
        if total_value >= 50000:
            vault_stats.append("<:PIRATES:1438231801859670107> **Wealthy Pirate**")
        if len(inv) >= 20:
            vault_stats.append("<:pirates:1438231834088701982> **Diverse Collector**")
        
        if vault_stats:
            embed.add_field(
                name="<a:captains_compass:1439449312269701232> **VAULT ACHIEVEMENTS**",
                value="\n".join(vault_stats),
                inline=False
            )

        embed.set_footer(text="Every treasure tells a story of your pirate journey! <a:dance_of_pirates:1438237492963840150>")
        
        await interaction.response.send_message(embed=embed)

    return