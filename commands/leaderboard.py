# commands/leaderboard.py
from discord import app_commands, Embed, Interaction

async def setup(bot, data):
    @bot.tree.command(name="leaderboard", description="See top pirates by gold.")
    async def leaderboard(interaction: Interaction):
        all_users = data.all_users()
        # sort by coins descending
        ranked = sorted(all_users.items(), key=lambda kv: kv[1].get("coins", 0), reverse=True)[:10]
        
        embed = Embed(
            title="<a:HUB_pirate_flag:1438231887532265482> **PIRATE KING LEADERBOARD**", 
            description="*The most feared treasure hunters across the seven seas*",
            color=0x8B4513
        )
        
        rank_emojis = [
            "<:pro:1392576041876324502>",
            "<:rookie:1392576056971493619>", 
            "<:elite:1392576075090890924>",
            "<:veteran:1392576091608055958>",
            "<:legendary:1392576106489708625>",
            "<:master:1392576120569856001>"
        ]
        
        for i, (uid, udata) in enumerate(ranked, start=1):
            try:
                member = await bot.fetch_user(int(uid))
                name = member.display_name
            except Exception:
                name = f"Pirate {uid[-4:]}"
            
            rank_emoji = rank_emojis[min(i-1, 5)]
            coins = udata.get("coins", 0)
            title = udata.get("title", "Deck Swabber")
            
            # Create unique card-style entry
            embed.add_field(
                name=f"{rank_emoji} **#{i} {name}**",
                value=(
                    f"<:Pirate_Coin:1439446496645746740> **{coins:,} gold**\n"
                    f"<:pirate_reviewer:1438237310708617386> **{title}**\n"
                    f"╰─ <a:Coins:1438241147540475945> Treasure Hoarder"
                ),
                inline=False
            )
        
        embed.set_footer(text="Climb the ranks by looting more treasure, matey! <a:dance_of_pirates:1438237492963840150>")
        await interaction.response.send_message(embed=embed)
    return