import nextcord, sqlite_func
from nextcord.ext import commands


class botCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
        
    @nextcord.slash_command(name="set_admin_role", description="Set the admin role so only admins can use commands")
    async def set_channel(self, interaction: nextcord.Interaction, role: nextcord.Role):
        global channel_id
        admin_role = role.id
        guild_id = self.interaction.guild.id
        sqlite_func.set_role_id(guild_id, admin_role)
        await interaction.response.send_message(f"Admin role set to {role.name}")