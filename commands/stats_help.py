# commands/stats_help.py
from discord import app_commands, Embed, Interaction
from utils import TITLES, get_user_title, LOOT_ITEMS
import time

async def setup(bot, data):
    @bot.tree.command(name="stats", description="View your legendary pirate career statistics.")
    async def stats(interaction: Interaction):
        user_id = str(interaction.user.id)
        user = data.get_user(user_id)
        
        # Calculate advanced statistics
        coins = user.get('coins', 0)
        total_loots = user.get('total_loots', 0)
        missions_completed = user.get('missions_completed', 0)
        biggest_haul = user.get('biggest_loot', 0)
        current_title = user.get('title', 'Deck Swabber')
        
        # Calculate item rarity breakdown
        inventory = user.get('inventory', {})
        mythic_count = sum(count for item, count in inventory.items() 
                          if any(loot["name"] == item and loot.get("value", 0) >= 500 
                                for loot_list in LOOT_ITEMS.values() for loot in loot_list))
        legendary_count = sum(count for item, count in inventory.items() 
                             if any(loot["name"] == item and 200 <= loot.get("value", 0) < 500 
                                   for loot_list in LOOT_ITEMS.values() for loot in loot_list))
        epic_count = sum(count for item, count in inventory.items() 
                        if any(loot["name"] == item and 100 <= loot.get("value", 0) < 200 
                              for loot_list in LOOT_ITEMS.values() for loot in loot_list))
        
        # Calculate success rates
        success_rate = min(100, int((missions_completed / (missions_completed + user.get('missions_failed', 0))) * 100)) if missions_completed > 0 else 0
        
        # Determine pirate legacy level
        if coins >= 100000:
            legacy_level = "<:master:1392576120569856001> **GHOST ADMIRAL LEGACY**"
            legacy_color = 0xFF0000
        elif coins >= 50000:
            legacy_level = "<:legendary:1392576106489708625> **PIRATE LORD LEGEND**"
            legacy_color = 0xFF4500
        elif coins >= 25000:
            legacy_level = "<:veteran:1392576091608055958> **CAPTAIN'S CHRONICLE**"
            legacy_color = 0xFFD700
        elif coins >= 10000:
            legacy_level = "<:elite:1392576075090890924> **QUARTERMASTER'S SAGA**"
            legacy_color = 0x00FF00
        elif coins >= 5000:
            legacy_level = "<:rookie:1392576056971493619> **FIRST MATE'S TALE**"
            legacy_color = 0x1E90FF
        else:
            legacy_level = "<:pro:1392576041876324502> **DECK SWABBER'S LOG**"
            legacy_color = 0x8B4513

        embed = Embed(
            title=f"<a:HUB_pirate_flag:1438231887532265482> **{interaction.user.display_name.upper()}'S PIRATE LEGACY**",
            description=legacy_level,
            color=legacy_color
        )

        # CORE STATISTICS - PIRATE MANIFEST
        embed.add_field(
            name="<a:Coins:1438241147540475945> **TREASURE MANIFEST**",
            value=(
                f"<:Pirate_Coin:1439446496645746740> **Gold Amassed:** {coins:,}\n"
                f"<a:mystry_box_of_pirate:1438237227477110936> **Expeditions:** {total_loots}\n"
                f"<:Gold_Bars:1439446648756506656> **Record Haul:** {biggest_haul:,}"
            ),
            inline=False
        )

        # COMBAT & ADVENTURE RECORD
        embed.add_field(
            name="<:skull_token:1439449760124637295> **ADVENTURE RECORD**",
            value=(
                f"<:PIRATES:1438231801859670107> **Missions:** {missions_completed}\n"
                f"<a:curse_gem:1439446670810157116> **Success Rate:** {success_rate}%\n"
                f"<:pirate_reviewer:1438237310708617386> **Current Rank:** {current_title}"
            ),
            inline=True
        )

        # TREASURE COLLECTION BREAKDOWN
        embed.add_field(
            name="<a:treasure_chest:1439446705354313819> **TREASURE VAULT**",
            value=(
                f"<:master:1392576120569856001> **Mythic:** {mythic_count}\n"
                f"<:legendary:1392576106489708625> **Legendary:** {legendary_count}\n"
                f"<:veteran:1392576091608055958> **Epic:** {epic_count}\n"
                f"<:elite:1392576075090890924> **Total Items:** {sum(inventory.values())}"
            ),
            inline=True
        )

        # ACTIVE BOOSTS & STATUS
        status_lines = []
        boosts = user.get('boosts', {})
        if boosts.get('double_loot', 0) > time.time():
            time_left = boosts['double_loot'] - time.time()
            hours = int(time_left // 3600)
            status_lines.append(f"<a:curse_gem:1439446670810157116> **Double Loot:** {hours}h remaining")
        
        if user.get('active_mission'):
            mission = user['active_mission']
            time_left = mission['end_time'] - time.time()
            hours = int(time_left // 3600)
            status_lines.append(f"<a:captains_compass:1439449312269701232> **Active Mission:** {mission['name']} ({hours}h)")
        
        if status_lines:
            embed.add_field(
                name="<:kraken_eye:1439449340195242035> **CURRENT STATUS**",
                value="\n".join(status_lines),
                inline=False
            )

        # PIRATE ACHIEVEMENTS
        achievements = []
        if coins >= 50000:
            achievements.append("<:Black_Pearl:1439449434885980240> **Wealth Beyond Measure**")
        if missions_completed >= 50:
            achievements.append("<:Jack_Sparrow:1438231857857695834> **Master Adventurer**")
        if biggest_haul >= 1000:
            achievements.append("<a:flame_skull1:1438231187633078273> **Legendary Haul**")
        if mythic_count >= 3:
            achievements.append("<:Sea_Serpent:1439449470096900169> **Mythic Collector**")
        
        if achievements:
            embed.add_field(
                name="<:pirates:1438231834088701982> **PIRATE ACHIEVEMENTS**",
                value="\n".join(achievements),
                inline=False
            )

        embed.set_footer(text="Your legend grows with every treasure found! <a:dance_of_pirates:1438237492963840150>")
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="help", description="Learn the ways of the pirate life.")
    async def help_command(interaction: Interaction):
        embed = Embed(
            title="<a:HUB_pirate_flag:1438231887532265482> **CAPTAIN'S NAVIGATION GUIDE**",
            description="*Chart your course through the treacherous seas of piracy*",
            color=0x00FF00
        )

        # TREASURE HUNTING COMMANDS
        embed.add_field(
            name="<a:mystry_box_of_pirate:1438237227477110936> **TREASURE HUNTING**",
            value=(
                "`/loot` - Embark on treasure expeditions (1h)\n"
                "`/mission` - Accept dangerous pirate contracts\n"
                "`/daily` - Daily treasure voyage\n"
                "`/weekly` - Legendary weekly expedition"
            ),
            inline=False
        )

        # PIRATE MANAGEMENT
        embed.add_field(
            name="<a:Coins:1438241147540475945> **PIRATE MANAGEMENT**",
            value=(
                "`/balance` - View your treasure manifest\n"
                "`/inventory` - Display collected artifacts\n"
                "`/stats` - Review your pirate legacy\n"
                "`/leaderboard` - Compete for glory"
            ),
            inline=True
        )

        # ECONOMY & TRADING
        embed.add_field(
            name="<a:treasure_chest:1439446705354313819> **PIRATE ECONOMY**",
            value=(
                "`/shop` - Visit the black market\n"
                "`/buy` - Acquire rare items\n"
                "`/mission_check` - Check active missions"
            ),
            inline=True
        )

        # PIRATE EDUCATION
        embed.add_field(
            name="<:ghost_map:1439449396482674708> **PIRATE WISDOM**",
            value=(
                "• **Rarity Tiers:** Common → Uncommon → Rare → Epic → Legendary → Mythic\n"
                "• **Mission Risks:** Higher rewards = greater dangers\n"
                "• **Daily Voyages:** Weather and rivals affect outcomes\n"
                "• **Weekly Expeditions:** 30% failure rate, but massive rewards"
            ),
            inline=False
        )

        # PIRATE PROGRESSION
        embed.add_field(
            name="<:pirate_reviewer:1438237310708617386> **RANK PROGRESSION**",
            value=(
                "**Deck Swabber** → **Sailor** → **Gunner** → **First Mate**\n"
                "**Quartermaster** → **Captain** → **Pirate Lord** → **Ghost Admiral**"
            ),
            inline=False
        )

        embed.set_footer(text="Set sail for fortune and may the winds favor your journey! <a:dance_of_pirates:1438237492963840150>")
        await interaction.response.send_message(embed=embed)

    return