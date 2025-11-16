# commands/loot.py
import time
import random
import asyncio
from discord import app_commands, Embed, Interaction

from utils import LOOT_ITEMS, RARITIES, get_rarity, ITEM_TO_RARITY, get_user_title

async def setup(bot, data):
    @bot.tree.command(name="loot", description="Begin your treasure hunt adventure (1h cooldown).")
    async def loot(interaction: Interaction):
        user_id = str(interaction.user.id)
        user = data.get_user(user_id)
        now = time.time()
        if now - user.get("last_loot", 0) < 3600:
            embed = Embed(title="<a:flame_skull1:1438231187633078273> **HOLD YOUR ANCHORS!**", 
                         description="The seas need time to replenish treasures, matey!\nCome back in an hour for another hunt.",
                         color=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # EPIC HUNT INTRODUCTION
        embed = Embed(title="<a:HUB_pirate_flag:1438231887532265482> **TREASURE HUNT INITIATED**", 
                     description="*You set sail into mysterious waters...*\n\n**Phase 1:** Scanning the horizon for wreckage...",
                     color=0x8B4513)
        embed.set_thumbnail(url="https://i.imgur.com/ship.gif")
        await interaction.response.send_message(embed=embed)
        
        # PHASE 1: LOCATION DISCOVERY
        await asyncio.sleep(2.5)
        locations = ["Shipwreck Cove", "Kraken's Depth", "Ghost Island", "Coral Caverns", "Siren's Reef"]
        chosen_location = random.choice(locations)
        
        embed = Embed(title="<:ghost_map:1439449396482674708> **LOCATION DISCOVERED**",
                     description=f"**{chosen_location}** appears on your map!\n\n**Phase 2:** Diving for the treasure chest...",
                     color=0x1E90FF)
        await interaction.edit_original_response(embed=embed)

        # PHASE 2: CHEST RECOVERY
        await asyncio.sleep(2.5)
        recovery_chance = random.randint(1, 100)
        
        if recovery_chance <= 15:  # 15% chance of failure
            failures = [
                "The Kraken attacked! You escaped empty-handed...",
                "A storm swept your treasure away!",
                "Rival pirates ambushed you!",
                "The chest was trapped! It sank to the depths..."
            ]
            embed = Embed(title="<:skull_token:1439449760124637295> **HUNT FAILED**",
                         description=f"**{random.choice(failures)}**\n\nBetter luck next time, sailor!",
                         color=0xff0000)
            data.set_timestamp(user_id, "last_loot", now)
            await data.save()
            await interaction.edit_original_response(embed=embed)
            return

        # SUCCESSFUL RECOVERY
        embed = Embed(title="<a:treasure_chest:1439446705354313819> **CHEST RECOVERED**",
                     description="You've pulled a ancient chest from the depths!\n\n**Phase 3:** Deciphering ancient locks...",
                     color=0xFFD700)
        await interaction.edit_original_response(embed=embed)

        # PHASE 3: UNLOCKING CHEST
        await asyncio.sleep(2.5)
        lock_difficulty = random.randint(1, 100)
        
        if lock_difficulty <= 25:  # 25% chance of lock failure
            embed = Embed(title="<a:captains_compass:1439449312269701232> **ANCIENT LOCKS**",
                         description="The chest's mechanisms are too complex...\nYou manage to salvage some coins from the exterior.",
                         color=0x808080)
            salvage_coins = random.randint(5, 20)
            data.add_coins(user_id, salvage_coins)
            data.set_timestamp(user_id, "last_loot", now)
            await data.save()
            
            embed.add_field(name="Salvaged Treasure", value=f"<:coin2_silver_piece:1439446611154571407> **{salvage_coins} coins**")
            await interaction.edit_original_response(embed=embed)
            return

        # EPIC CHEST OPENING - FINAL PHASE
        embed = Embed(title="<a:mystry_box_of_pirate:1438237227477110936> **UNLOCKING ANCIENT CHEST**",
                     description="The chest glows with mystical energy...\nAncient mechanisms click into place...",
                     color=0xFF4500)
        await interaction.edit_original_response(embed=embed)
        await asyncio.sleep(2.0)

        # DETERMINE LOOT WITH STRUGGLE MECHANICS
        rarity = get_rarity()
        
        # STRUGGLE SYSTEM: Higher rarity = lower chance to actually get it
        struggle_roll = random.randint(1, 100)
        struggle_success = True
        
        if rarity == "Legendary" and struggle_roll <= 40:  # 40% fail chance
            struggle_success = False
            loot_item = random.choice(LOOT_ITEMS["Rare"])
        elif rarity == "Mythic" and struggle_roll <= 60:  # 60% fail chance
            struggle_success = False
            loot_item = random.choice(LOOT_ITEMS["Epic"])
        elif rarity == "Epic" and struggle_roll <= 25:  # 25% fail chance
            struggle_success = False
            loot_item = random.choice(LOOT_ITEMS["Uncommon"])
        else:
            loot_item = random.choice(LOOT_ITEMS[rarity])

        base_value = loot_item["value"]

        # Check double-loot boost
        double_until = user.get("boosts", {}).get("double_loot", 0)
        final_value = base_value * 2 if double_until > now else base_value

        # Update user data
        data.add_coins(user_id, final_value)
        data.add_item(user_id, loot_item["name"], 1)
        data.set_timestamp(user_id, "last_loot", now)
        
        # Update title based on coins
        user_after = data.get_user(user_id)
        new_title = get_user_title(user_after["coins"])
        data.set_field(user_id, "title", new_title)

        await data.save()

        # EPIC RESULT REVEAL
        if not struggle_success:
            desc = f"**The treasure was cursed!**\n\n{ loot_item['emoji']} **{loot_item['name']}**\n*The ancient magic transformed your find...*"
            color = 0x800080  # Purple for cursed
        else:
            desc = f"**{loot_item['emoji']} {loot_item['name']}**\n*{loot_item['flavor']}*"
            color = RARITIES[rarity]["color"]

        result = Embed(title=f"{RARITIES[rarity]['emoji']} **{rarity.upper()} TREASURE!**", 
                      description=desc, 
                      color=color)
        
        result.add_field(name="<:Pirate_Coin:1439446496645746740> Value", 
                        value=f"**{final_value} coins** {'<a:Coins:1438241147540475945> **DOUBLED!**' if final_value > base_value else ''}", 
                        inline=True)
        
        result.add_field(name="<:pirate_reviewer:1438237310708617386> Rank", 
                        value=f"**{new_title}**", 
                        inline=True)
        
        if not struggle_success:
            result.add_field(name="<a:skulleysshit:1438231756699603106> Ancient Curse", 
                           value="The treasure transformed during recovery!", 
                           inline=False)
        
        result.set_footer(text=f"Hunt Location: {chosen_location} | Total Expeditions: {user_after.get('total_loots', 0) + 1}")

        # SPECIAL EFFECTS FOR HIGH RARITY
        if rarity in ["Legendary", "Mythic"] and struggle_success:
            await interaction.edit_original_response(embed=result)
            # Send epic announcement
            announcement = Embed(title="<a:flame_skull1:1438231187633078273> **LEGENDARY FIND!**",
                               description=f"**{interaction.user.display_name}** discovered {loot_item['emoji']} **{loot_item['name']}** at {chosen_location}!",
                               color=0xFFD700)
            await interaction.followup.send(embed=announcement)
        else:
            await interaction.edit_original_response(embed=result)

    return