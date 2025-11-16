# commands/daily_weekly.py
import time
import random
import asyncio
from discord import app_commands, Embed, Interaction

async def setup(bot, data):
    @bot.tree.command(name="daily", description="Embark on your daily treasure voyage.")
    async def daily(interaction: Interaction):
        user_id = str(interaction.user.id)
        user = data.get_user(user_id)
        now = time.time()
        
        # Check cooldown with pirate flavor
        if now - user.get("last_daily", 0) < 86400:
            next_claim = user["last_daily"] + 86400
            time_left = next_claim - now
            hours = int(time_left // 3600)
            minutes = int((time_left % 3600) // 60)
            
            embed = Embed(
                title="<a:flame_skull1:1438231187633078273> **DAILY VOYAGE DENIED**",
                description="The tides aren't right for another expedition yet!",
                color=0xff0000
            )
            embed.add_field(
                name="<:pirate_reviewer:1438237310708617386> Next Voyage Available",
                value=f"**{hours}h {minutes}m** from now",
                inline=False
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # DAILY TREASURE HUNT MINI-GAME
        embed = Embed(
            title="<a:HUB_pirate_flag:1438231887532265482> **DAILY TREASURE VOYAGE**",
            description="*Setting sail for today's bounty...*\n\n**Scanning the horizon for opportunities...**",
            color=0x8B4513
        )
        await interaction.response.send_message(embed=embed)
        
        # VOYAGE PHASE 1: WEATHER CHECK
        await asyncio.sleep(2)
        weather_roll = random.randint(1, 100)
        if weather_roll <= 20:  # 20% chance of bad weather
            embed = Embed(
                title="<:skull_token:1439449760124637295> **STORMY SEAS**",
                description="A sudden storm forces you back to port! Reduced bounty...",
                color=0x1E90FF
            )
            bonus = random.randint(50, 100)
            data.add_coins(user_id, bonus)
            data.set_timestamp(user_id, "last_daily", now)
            embed.add_field(
                name="<:coin2_silver_piece:1439446611154571407> Salvaged Treasure",
                value=f"**{bonus} gold** from nearby waters",
                inline=False
            )
            await interaction.edit_original_response(embed=embed)
            await data.save()
            return
        
        # VOYAGE PHASE 2: LOCATION DISCOVERY
        await asyncio.sleep(2)
        locations = [
            {"name": "Sunken Galleon", "multiplier": 1.5, "emoji": "<a:treasure_chest:1439446705354313819>"},
            {"name": "Pirate Outpost", "multiplier": 1.2, "emoji": "<:PIRATES:1438231801859670107>"},
            {"name": "Trade Route", "multiplier": 1.0, "emoji": "⛵"},
            {"name": "Hidden Cove", "multiplier": 1.8, "emoji": "<:ghost_map:1439449396482674708>"},
            {"name": "Ancient Temple", "multiplier": 2.0, "emoji": "<a:curse_gem:1439446670810157116>"}
        ]
        location = random.choice(locations)
        
        embed = Embed(
            title=f"{location['emoji']} **TREASURE LOCATION FOUND**",
            description=f"**{location['name']}** appears on your maps!",
            color=0xFFD700
        )
        embed.add_field(
            name="<:pirate_reviewer:1438237310708617386> Location Multiplier",
            value=f"**{location['multiplier']}x** bounty potential",
            inline=True
        )
        await interaction.edit_original_response(embed=embed)
        
        # VOYAGE PHASE 3: RECOVERY CHALLENGE
        await asyncio.sleep(2)
        challenge_roll = random.randint(1, 100)
        
        if challenge_roll <= 15:  # 15% chance of rival pirates
            embed = Embed(
                title="<:pirates:1438231834088701982> **RIVAL PIRATES!**",
                description="Another crew reached the treasure first! You only get a share...",
                color=0xff0000
            )
            base_bonus = random.randint(80, 150)
            bonus = int(base_bonus * 0.3)  # Only 30% of potential
            data.add_coins(user_id, bonus)
            data.set_timestamp(user_id, "last_daily", now)
            embed.add_field(
                name="<:coin2_silver_piece:1439446611154571407> Your Share",
                value=f"**{bonus} gold** after the split",
                inline=False
            )
            await interaction.edit_original_response(embed=embed)
            await data.save()
            return
        
        # SUCCESSFUL RECOVERY
        base_bonus = random.randint(150, 300)
        bonus = int(base_bonus * location['multiplier'])
        
        # SPECIAL BONUS CHANCE (10%)
        special_bonus = 0
        if random.randint(1, 100) <= 10:
            special_bonus = random.randint(100, 200)
            bonus += special_bonus
        
        data.add_coins(user_id, bonus)
        data.set_timestamp(user_id, "last_daily", now)
        
        embed = Embed(
            title="<a:dance_of_pirates:1438237492963840150> **VOYAGE SUCCESS!**",
            description=f"**{location['name']}** yielded incredible treasures!",
            color=0x00FF00
        )
        
        reward_text = f"<:Pirate_Coin:1439446496645746740> Base: **{base_bonus} gold**\n"
        reward_text += f"{location['emoji']} Multiplier: **{location['multiplier']}x**\n"
        reward_text += f"<:Gold_Bars:1439446648756506656> Total: **{bonus} gold**"
        
        if special_bonus > 0:
            reward_text += f"\n<a:Coins:1438241147540475945> **BONUS:** +{special_bonus} gold!"
        
        embed.add_field(
            name="<a:Coins:1438241147540475945> Treasure Recovered",
            value=reward_text,
            inline=False
        )
        
        embed.set_footer(text="Return tomorrow for another voyage across the seven seas!")
        await interaction.edit_original_response(embed=embed)
        await data.save()

    @bot.tree.command(name="weekly", description="Embark on your weekly legendary expedition.")
    async def weekly(interaction: Interaction):
        user_id = str(interaction.user.id)
        user = data.get_user(user_id)
        now = time.time()
        
        # Check cooldown
        if now - user.get("last_weekly", 0) < 604800:
            next_claim = user["last_weekly"] + 604800
            time_left = next_claim - now
            days = int(time_left // 86400)
            hours = int((time_left % 86400) // 3600)
            
            embed = Embed(
                title="<a:flame_skull1:1438231187633078273> **LEGENDARY EXPEDITION DENIED**",
                description="Such grand adventures require proper planning and rest!",
                color=0xff0000
            )
            embed.add_field(
                name="<:pirate_reviewer:1438237310708617386> Next Expedition Available",
                value=f"**{days}d {hours}h** from now",
                inline=False
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # WEEKLY LEGENDARY EXPEDITION
        embed = Embed(
            title="<:master:1392576120569856001> **LEGENDARY WEEKLY EXPEDITION**",
            description="*Preparing for a voyage that will be sung about for ages...*\n\n**Gathering your most trusted crew and supplies...**",
            color=0x800080
        )
        await interaction.response.send_message(embed=embed)
        
        # EXPEDITION PHASE 1: LEGENDARY LOCATION
        await asyncio.sleep(3)
        legendary_locations = [
            {"name": "Dragon Turtle's Lair", "base_reward": 800, "emoji": "<:Sea_Serpent:1439449470096900169>", "danger": "Extreme"},
            {"name": "Kraken's Breeding Ground", "base_reward": 700, "emoji": "<:kraken_eye:1439449340195242035>", "danger": "Deadly"},
            {"name": "Ghost Fleet Graveyard", "base_reward": 900, "emoji": "<a:flame_skull1:1438231187633078273>", "danger": "Haunted"},
            {"name": "Leviathan's Domain", "base_reward": 1000, "emoji": "<:Black_Pearl:1439449434885980240>", "danger": "Mythical"}
        ]
        location = random.choice(legendary_locations)
        
        embed = Embed(
            title=f"{location['emoji']} **LEGENDARY DESTINATION**",
            description=f"**{location['name']}** - A place few dare to venture!",
            color=0xFF4500
        )
        embed.add_field(
            name="<:skull_token:1439449760124637295> Danger Level",
            value=f"**{location['danger']}**",
            inline=True
        )
        embed.add_field(
            name="<a:Coins:1438241147540475945> Potential Reward",
            value=f"**{location['base_reward']}+ gold**",
            inline=True
        )
        await interaction.edit_original_response(embed=embed)
        
        # EXPEDITION PHASE 2: SURVIVAL CHALLENGE
        await asyncio.sleep(3)
        survival_roll = random.randint(1, 100)
        
        if survival_roll <= 30:  # 30% chance of expedition disaster
            disasters = [
                "The ancient guardian awoke and destroyed your fleet!",
                "A cursed storm swallowed your ships whole!",
                "Mythical sea creatures decimated your crew!",
                "The treasure was protected by eternal magic!"
            ]
            
            embed = Embed(
                title="<:skull_token:1439449760124637295> **EXPEDITION DISASTER**",
                description=f"**{location['name']}** proved too dangerous!",
                color=0xff0000
            )
            embed.add_field(
                name="<a:flame_skull1:1438231187633078273> What Happened",
                value=f"*{random.choice(disasters)}*",
                inline=False
            )
            
            # Small survival bonus
            survival_bonus = location['base_reward'] // 5
            data.add_coins(user_id, survival_bonus)
            data.set_timestamp(user_id, "last_weekly", now)
            
            embed.add_field(
                name="<:coin2_silver_piece:1439446611154571407> Survival Bonus",
                value=f"**{survival_bonus} gold** for making it back alive",
                inline=False
            )
            
            await interaction.edit_original_response(embed=embed)
            await data.save()
            return
        
        # EXPEDITION SUCCESS - LEGENDARY REWARDS
        base_bonus = random.randint(location['base_reward'], location['base_reward'] + 500)
        
        # BONUS MULTIPLIERS BASED ON LUCK
        luck_roll = random.randint(1, 100)
        multiplier = 1.0
        
        if luck_roll <= 10:  # 10% chance for jackpot
            multiplier = 2.0
            bonus_type = "<:legendary:1392576106489708625> **JACKPOT!**"
        elif luck_roll <= 30:  # 20% chance for great find
            multiplier = 1.5
            bonus_type = "<:veteran:1392576091608055958> **Great Find!**"
        else:  # 70% chance for standard
            multiplier = 1.0
            bonus_type = "<:elite:1392576075090890924> **Standard Reward**"
        
        total_bonus = int(base_bonus * multiplier)
        
        data.add_coins(user_id, total_bonus)
        data.set_timestamp(user_id, "last_weekly", now)
        
        embed = Embed(
            title="<a:dance_of_pirates:1438237492963840150> **LEGENDARY SUCCESS!**",
            description=f"You conquered **{location['name']}** and returned with unimaginable treasures!",
            color=0xFFD700
        )
        
        reward_text = f"{location['emoji']} Base: **{base_bonus} gold**\n"
        reward_text += f"{bonus_type} Multiplier: **{multiplier}x**\n"
        reward_text += f"<a:Coins:1438241147540475945> **TOTAL: {total_bonus} GOLD**"
        
        embed.add_field(
            name="<:Gold_Bars:1439446648756506656> Expedition Rewards",
            value=reward_text,
            inline=False
        )
        
        if multiplier >= 2.0:
            embed.add_field(
                name="<:Jack_Sparrow:1438231857857695834> Legendary Achievement",
                value="Your name will be remembered in pirate tales forever!",
                inline=False
            )
        
        embed.set_footer(text="Such legendary feats require a week to recover... return then!")
        await interaction.edit_original_response(embed=embed)
        await data.save()

    return