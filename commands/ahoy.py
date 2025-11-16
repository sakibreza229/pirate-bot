# commands/ahoy.py
from discord import app_commands, Interaction

async def setup(bot, data):
    @bot.tree.command(name="ahoy", description="Replies with ahoy, mate!")
    async def ahoy(interaction: Interaction):
        await interaction.response.send_message(
            "ahoy, matey! <a:yo_mf_pirate:1438239420900839584>"
        )
