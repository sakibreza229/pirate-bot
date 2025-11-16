import discord

async def setup(bot, data):
    @bot.tree.command(name="inquire", description="Learn about Captain bot and how to become a pirate legend!")
    async def inquire(interaction: discord.Interaction):
        embed = discord.Embed(
            title="<a:HUB_pirate_flag:1438231887532265482> **WELCOME TO CAPTAIN BOT**",
            description="*The ultimate pirate looting adventure on Discord!*",
            color=0xFFD700
        )
        
        embed.add_field(
            name="<:12023staff:1392558969439916158> **What is Captain Bot?**",
            value="""Captain Bot is your digital pirate companion that brings the thrill of treasure hunting to your server! Every hour, you can open mystery chests filled with gold, rare artifacts, and legendary items from across the seven seas.""",
            inline=False
        )
        
        embed.add_field(
            name="<a:Verified:1392557971204210750> **How Does It Work?**",
            value="""**1.** Use `/loot` every hour to open treasure chests
**2.** Discover coins and rare items with different rarities
**3.** Complete pirate missions with `/mission` for extra rewards
**4.** Claim daily and weekly bonuses for consistent loot
**5.** Buy special items from the shop with your earnings
**6.** Climb the leaderboard to become the most feared pirate!""",
            inline=False
        )
        
        embed.add_field(
            name="<:76998diamond:1392559386333020261> **Why You'll Love It**",
            value="""• **Addictive Looting** - That thrill of opening a chest never gets old!
• **Rare Collectibles** - Hunt for Mythic items with 0.5% drop rates!
• **Pirate Progression** - Rise from Deck Swabber to Ghost Admiral!
• **Server Competition** - Battle friends for the top spot on the leaderboard!
• **Daily Adventure** - New missions and treasures await every day!""",
            inline=False
        )
        
        embed.add_field(
            name="<:2374booster:1392560062890770464> **The Pirate's Joy**",
            value="""Every 'click' of `/loot` could reveal a life-changing treasure! That moment when the chest glows **LEGENDARY** and the server erupts in celebration... that's the magic of being a pirate! The chase for the next big score, the pride of your growing collection, the respect of your crew - this is what makes every day an adventure worth sailing for!""",
            inline=False
        )
        
        embed.add_field(
            name="<:14448giveaway:1392559008778555412> **Getting Started**",
            value="""Simply use `/loot` to begin your journey! Check `/help` for all commands, and remember - the greatest pirates are those who never stop hunting!""",
            inline=False
        )
        
        embed.set_footer(text="Set sail for fortune and glory! The seven seas await your command!")
        
        await interaction.response.send_message(embed=embed)
