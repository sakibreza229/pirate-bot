# commands/missions.py
import random
import time
from typing import Optional
from discord import app_commands, Embed, Interaction, Message
import discord

# Detailed mission definitions (same as your original list)
PIRATE_MISSIONS = [
    {
        "name": "Plunder Merchant Vessel",
        "difficulty": "<:pro:1392576041876324502> Easy",
        "reward": 80,
        "emoji": "<:PIRATES:1438231801859670107>",
        "description": "Attack a wealthy merchant ship sailing through trade routes",
        "challenge": "Royal Navy patrols nearby",
        "duration": 3
    },
    {
        "name": "Buried Island Treasure",
        "difficulty": "<:rookie:1392576056971493619> Medium",
        "reward": 180,
        "emoji": "<:ghost_map:1439449396482674708>",
        "description": "Follow ancient maps to hidden island treasure",
        "challenge": "Cursed guardians protect the treasure",
        "duration": 5
    },
    {
        "name": "Kraken Hunt",
        "difficulty": "<:elite:1392576075090890924> Hard",
        "reward": 350,
        "emoji": "<:kraken_eye:1439449340195242035>",
        "description": "Hunt the legendary sea monster in deep waters",
        "challenge": "Kraken's tentacles can crush ships",
        "duration": 8
    },
    {
        "name": "Storm Navy Fortress",
        "difficulty": "<:veteran:1392576091608055958> Expert",
        "reward": 600,
        "emoji": "<a:HUB_pirate_flag:1438231887532265482>",
        "description": "Attack heavily fortified royal navy stronghold",
        "challenge": "Cannons and trained soldiers defend",
        "duration": 12
    },
    {
        "name": "Ghost Ship Recovery",
        "difficulty": "<:legendary:1392576106489708625> Legendary",
        "reward": 1000,
        "emoji": "<a:flame_skull1:1438231187633078273>",
        "description": "Board a haunted ghost ship lost for centuries",
        "challenge": "Spectral crew defends their eternal vessel",
        "duration": 15
    },
    {
        "name": "Dragon Turtle Hunt",
        "difficulty": "<:master:1392576120569856001> Mythic",
        "reward": 2000,
        "emoji": "<:Sea_Serpent:1439449470096900169>",
        "description": "Hunt the ancient dragon turtle of the abyss",
        "challenge": "Breathes fire and summons whirlpools",
        "duration": 20
    }
]

# Use a simple unicode reaction for acceptance to avoid custom-emoji lookup issues
ACCEPT_EMOJI = "🏴‍☠️"

async def setup(bot, data):
    """
    Register slash commands and reaction listener.
    `data` is expected to be your DataManager instance with:
      - get_user(user_id)
      - add_coins(user_id, amount)
      - set_timestamp(user_id, key, value)
      - save()
    """

    @bot.tree.command(name="mission", description="Embark on a dangerous pirate expedition.")
    async def mission(interaction: Interaction):
        user_id = str(interaction.user.id)
        user = data.get_user(user_id)

        # Check for an active mission
        active = user.get("active_mission")
        now = time.time()
        if active and active.get("end_time", 0) > now:
            time_left = active["end_time"] - now
            hours = int(time_left // 3600)
            minutes = int((time_left % 3600) // 60)
            embed = Embed(
                title="<a:captains_compass:1439449312269701232> **MISSION IN PROGRESS**",
                description=f"You're already on a mission: **{active.get('name')}**",
                color=0xFFA500
            )
            embed.add_field(name="Time Remaining", value=f"**{hours}h {minutes}m**", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Choose a mission
        mission_def = random.choice(PIRATE_MISSIONS)

        embed = Embed(
            title=f"{mission_def['emoji']} **PIRATE EXPEDITION BRIEFING**",
            description="*A new opportunity arises on the horizon...*",
            color=0x8B4513
        )
        embed.add_field(name="<a:HUB_pirate_flag:1438231887532265482> MISSION", value=f"**{mission_def['name']}**", inline=False)
        embed.add_field(name="<:skull_token:1439449760124637295> DIFFICULTY", value=mission_def["difficulty"], inline=True)
        embed.add_field(name="<a:Coins:1438241147540475945> BOUNTY", value=f"<:Pirate_Coin:1439446496645746740> **{mission_def['reward']} gold**", inline=True)
        embed.add_field(name="<:ghost_map:1439449396482674708> OBJECTIVE", value=f"*{mission_def['description']}*", inline=False)
        embed.add_field(name="<a:curse_gem:1439446670810157116> CHALLENGE", value=f"*{mission_def['challenge']}*", inline=False)
        embed.add_field(name="⏱️ DURATION", value=f"**{mission_def['duration']} hours**", inline=True)
        embed.set_footer(text=f"React with {ACCEPT_EMOJI} to accept this dangerous mission!")

        # Send the briefing and add the reaction
        await interaction.response.send_message(embed=embed)
        try:
            msg: Optional[Message] = await interaction.original_response()
            # Add a unicode reaction to avoid custom-emoji resolution issues
            await msg.add_reaction(ACCEPT_EMOJI)
        except Exception:
            # If original_response fails, ignore reaction add (command still works)
            pass

    # Reaction listener for mission acceptance.
    async def on_reaction_add(reaction, user):
        # Ignore bot reactions
        if user.bot:
            return

        # Only accept the designated emoji
        try:
            emoji_ok = False
            # reaction.emoji can be str (for unicode) or PartialEmoji/Emoji for custom
            if isinstance(reaction.emoji, str):
                emoji_ok = reaction.emoji == ACCEPT_EMOJI
            else:
                # If custom emoji was used in embed, also allow it in case guild-specific emoji was used
                # But primary acceptance relies on the unicode emoji we add after sending the embed.
                emoji_ok = reaction.emoji.name == "PIRATES" or reaction.emoji.id == 1438231801859670107
        except Exception:
            return

        if not emoji_ok:
            return

        message = reaction.message
        if not message.embeds:
            return

        embed = message.embeds[0]
        if "PIRATE EXPEDITION BRIEFING" not in (embed.title or ""):
            return

        guild = getattr(message, "guild", None)
        channel = message.channel

        # Determine which mission was presented by parsing the embed fields
        mission_name = None
        mission_reward = 0
        mission_duration = 0
        for field in embed.fields:
            name_lower = field.name.lower()
            if "mission" in name_lower:
                # field.value expected like "**Name**"
                mission_name = field.value.strip()
                # remove surrounding asterisks if present
                if mission_name.startswith("**") and mission_name.endswith("**"):
                    mission_name = mission_name[2:-2].strip()
            elif "bounty" in name_lower:
                # field.value includes digits; extract them
                try:
                    mission_reward = int(''.join(ch for ch in field.value if ch.isdigit()))
                except Exception:
                    mission_reward = 0
            elif "duration" in name_lower:
                try:
                    mission_duration = int(''.join(ch for ch in field.value if ch.isdigit()))
                except Exception:
                    mission_duration = 0

        if not mission_name:
            # fallback: try to match by title or return
            return

        user_id = str(user.id)
        user_data = data.get_user(user_id)
        now = time.time()

        # Check if user already has active mission
        active = user_data.get("active_mission")
        if active and active.get("end_time", 0) > now:
            await channel.send(f"{user.mention} You're already on a mission, matey!", delete_after=8)
            return

        # Start mission: calculate end_time in seconds (duration hours)
        end_time = now + (mission_duration * 3600)
        user_data["active_mission"] = {
            "name": mission_name,
            "start_time": now,
            "end_time": end_time,
            "reward": mission_reward,
            "duration": mission_duration
        }

        # Confirmation embed
        conf = Embed(
            title="<a:mystry_box_of_pirate:1438237227477110936> **MISSION ACCEPTED**",
            description=f"**{user.display_name}** has embarked on **{mission_name}**!",
            color=0x00FF00
        )
        conf.add_field(name="Estimated Return", value=f"<t:{int(end_time)}:R>", inline=False)
        conf.add_field(name="Potential Reward", value=f"<:Pirate_Coin:1439446496645746740> **{mission_reward} gold**", inline=True)
        conf.add_field(name="Risk Level", value="**High** - Many don't return...", inline=True)
        conf.set_footer(text="The seas are dangerous... return alive with your bounty!")

        # persist
        await data.save()

        try:
            await channel.send(embed=conf)
        except Exception:
            pass

    # Register listener using bot.add_listener to avoid multiple event definitions
    bot.add_listener(on_reaction_add, "on_reaction_add")

    # Slash command to check mission status and handle completion
    @bot.tree.command(name="mission_check", description="Check your current mission status.")
    async def mission_check(interaction: Interaction):
        user_id = str(interaction.user.id)
        user_data = data.get_user(user_id)
        active = user_data.get("active_mission")
        now = time.time()

        if not active:
            embed = Embed(
                title="<:skull_token:1439449760124637295> **NO ACTIVE MISSION**",
                description="You're not on any mission currently.\nUse `/mission` to find new opportunities!",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        mission_end = active.get("end_time", 0)
        mission_name = active.get("name", "Unknown")
        mission_reward = int(active.get("reward", 0))

        if now >= mission_end:
            # mission finished: determine outcome
            success_chance = random.randint(1, 100)
            if success_chance <= 75:  # success
                bonus = random.randint(0, max(0, mission_reward // 2))
                total_reward = mission_reward + bonus
                data.add_coins(user_id, total_reward)
                user_data["missions_completed"] = user_data.get("missions_completed", 0) + 1
                user_data["total_mission_rewards"] = user_data.get("total_mission_rewards", 0) + total_reward
                # clear active mission
                del user_data["active_mission"]

                embed = Embed(
                    title="<a:dance_of_pirates:1438237492963840150> **MISSION ACCOMPLISHED!**",
                    description=f"**{mission_name}** completed successfully!",
                    color=0x00FF00
                )
                embed.add_field(
                    name="Rewards Earned",
                    value=(
                        f"Base: **{mission_reward} gold**\n"
                        f"Bonus: **{bonus} gold**\n"
                        f"**Total: {total_reward} gold**"
                    ),
                    inline=False
                )
            else:
                # failure: small consolation
                consolation = mission_reward // 4
                data.add_coins(user_id, consolation)
                user_data["missions_completed"] = user_data.get("missions_completed", 0) + 0  # not incrementing
                user_data["total_mission_rewards"] = user_data.get("total_mission_rewards", 0) + consolation
                del user_data["active_mission"]

                embed = Embed(
                    title="<a:flame_skull1:1438231187633078273> **MISSION FAILED**",
                    description=f"**{mission_name}** ended in disaster!",
                    color=0xff0000
                )
                failure_reasons = [
                    "Your ship was damaged in battle",
                    "Rival pirates stole your bounty",
                    "A storm destroyed your supplies",
                    "The treasure was cursed and lost",
                    "Navy reinforcements arrived"
                ]
                embed.add_field(name="What Happened", value=f"*{random.choice(failure_reasons)}*", inline=False)
                embed.add_field(name="Consolation", value=f"Salvaged **{consolation} gold** from the wreckage", inline=True)

            await data.save()
            await interaction.response.send_message(embed=embed)
            return
        else:
            # still in progress
            time_left = mission_end - now
            hours = int(time_left // 3600)
            minutes = int((time_left % 3600) // 60)
            embed = Embed(
                title="<a:captains_compass:1439449312269701232> **MISSION IN PROGRESS**",
                description=f"**{mission_name}**",
                color=0xFFA500
            )
            embed.add_field(name="Time Remaining", value=f"**{hours}h {minutes}m**", inline=True)
            embed.add_field(name="Potential Reward", value=f"<:Pirate_Coin:1439446496645746740> **{mission_reward} gold**", inline=True)
            embed.add_field(name="Estimated Return", value=f"<t:{int(mission_end)}:R>", inline=False)
            await interaction.response.send_message(embed=embed)

    return
