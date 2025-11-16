# commands/balance.py
from discord import app_commands, Embed, Interaction
from utils import TITLES
import time
from utils import LOOT_ITEMS

async def setup(bot, data):
    @bot.tree.command(name="balance", description="Check your treasure hoard.")
    async def balance(interaction: Interaction):
        user_id = str(interaction.user.id)
        user = data.get_user(user_id)
        
        # Calculate treasure tiers based on coin amount
        coins = user.get('coins', 0)
        if coins >= 100000:
            treasure_level = "<:master:1392576120569856001> **GHOST ADMIRAL'S FORTUNE**"
            color = 0xFF0000
        elif coins >= 50000:
            treasure_level = "<:legendary:1392576106489708625> **PIRATE LORD'S HOARD**"
            color = 0xFF4500
        elif coins >= 25000:
            treasure_level = "<:veteran:1392576091608055958> **CAPTAIN'S TREASURE**"
            color = 0xFFD700
        elif coins >= 10000:
            treasure_level = "<:elite:1392576075090890924> **QUARTERMASTER'S STASH**"
            color = 0x00FF00
        elif coins >= 5000:
            treasure_level = "<:rookie:1392576056971493619> **FIRST MATE'S BOUNTY**"
            color = 0x1E90FF
        elif coins >= 1000:
            treasure_level = "<:pro:1392576041876324502> **GUNNER'S EARNINGS**"
            color = 0x808080
        else:
            treasure_level = "⚓ **DECK SWABBER'S SAVINGS**"
            color = 0x8B4513

        embed = Embed(
            title=f"<a:Coins:1438241147540475945> **{interaction.user.display_name.upper()}'S TREASURE MANIFEST**",
            description=f"{treasure_level}",
            color=color
        )

        # MAIN TREASURE DISPLAY - PIRATE STYLE
        embed.add_field(
            name="<:Pirate_Coin:1439446496645746740> **GOLD PIECES**",
            value=f"<a:Coins:1438241147540475945>{coins:,} GOLD <a:Coins:1438241147540475945> ",
            inline=False
        )

        # TREASURE BREAKDOWN
        if user.get("inventory"):
            legendary_items = sum(count for item, count in user["inventory"].items() if any(loot["name"] == item and loot.get("value", 0) >= 200 for loot_list in LOOT_ITEMS.values() for loot in loot_list))
            epic_items = sum(count for item, count in user["inventory"].items() if any(loot["name"] == item and 100 <= loot.get("value", 0) < 200 for loot_list in LOOT_ITEMS.values() for loot in loot_list))
            rare_items = sum(count for item, count in user["inventory"].items() if any(loot["name"] == item and 50 <= loot.get("value", 0) < 100 for loot_list in LOOT_ITEMS.values() for loot in loot_list))
            
            embed.add_field(
                name="<a:treasure_chest:1439446705354313819> **TREASURE BREAKDOWN**",
                value=(
                    f"<:master:1392576120569856001> **Legendary:** {legendary_items}\n"
                    f"<:veteran:1392576091608055958> **Epic:** {epic_items}\n"
                    f"<:elite:1392576075090890924> **Rare:** {rare_items}\n"
                    f"<:pro:1392576041876324502> **Common:** {len(user['inventory']) - (legendary_items + epic_items + rare_items)}"
                ),
                inline=True
            )

        # RECENT ACQUISITIONS
        if user.get("inventory"):
            recent_items = list(user["inventory"].items())[-3:]  # Last 3 items
            recent_display = []
            for item_name, count in recent_items:
                # Find item emoji
                item_emoji = "📦"
                for rarity_items in LOOT_ITEMS.values():
                    for loot in rarity_items:
                        if loot["name"] == item_name:
                            item_emoji = loot["emoji"]
                            break
                recent_display.append(f"{item_emoji} **{item_name}** ×{count}")
            
            embed.add_field(
                name="<a:captains_compass:1439449312269701232> **RECENT FINDS**",
                value="\n".join(recent_display) if recent_display else "No recent treasures",
                inline=True
            )

        # PIRATE STATUS
        status_messages = []
        if user.get('boosts', {}).get('double_loot', 0) > time.time():
            status_messages.append("<a:curse_gem:1439446670810157116> **Double Loot Active**")
        if coins >= 50000:
            status_messages.append("<:Black_Pearl:1439449434885980240> **Elite Pirate**")
        elif coins >= 10000:
            status_messages.append("<:Sea_Serpent:1439449470096900169> **Veteran Sailor**")
        
        if status_messages:
            embed.add_field(
                name="<a:HUB_pirate_flag:1438231887532265482> **PIRATE STATUS**",
                value="\n".join(status_messages),
                inline=False
            )

        # TREASURE PROGRESSION BAR
        next_rank = None
        current_title = user.get('title', 'Deck Swabber')
        titles_list = list(TITLES.keys())
        current_index = titles_list.index(current_title) if current_title in titles_list else 0
        
        if current_index < len(titles_list) - 1:
            next_rank = titles_list[current_index + 1]
            next_requirement = TITLES[next_rank]["requirement"]
            progress = min(100, int((coins / next_requirement) * 100))
            
            # Create visual progress bar
            bars = 10
            filled_bars = progress // bars
            progress_bar = "█" * filled_bars + "▒" * (bars - filled_bars)
            
            embed.add_field(
                name=f"<:kraken_eye:1439449340195242035> **PROGRESS TO {next_rank.upper()}**",
                value=f"```[{progress_bar}] {progress}%```\n{coins:,} / {next_requirement:,} gold",
                inline=False
            )

        embed.set_footer(text="Keep hunting, the seven seas hold endless treasures! <a:dance_of_pirates:1438237492963840150>")
        
        await interaction.response.send_message(embed=embed)

    return