import nextcord, sqlite_func, functions, colorama, asyncio
#from bot_commands import botCommands
from nextcord.ext import commands
from colorama import Fore

# TODO
# Help and ping commands


colorama.init(autoreset=True)
bot = commands.Bot()
#bot.add_cog(botCommands(bot))

@bot.event
async def on_ready():
    print(Fore.GREEN + f"We have logged in as {bot.user} at {functions.gettime()}")
    
    
member_channels = {}  # Maps members to their channels and timers
channel_id = None  # Default channel ID
global_enable_voice_creation = False
global_enable_command_creation = False


@bot.slash_command(name="set_channel", description="Set the voice channel")
async def set_channel(interaction: nextcord.Interaction, channel: nextcord.VoiceChannel):
    guild_id = interaction.guild.id
    sqlite_func.add_guild_if_not_exists(guild_id)
    admin_role_id = sqlite_func.get_role_id(guild_id)
    admin_role = interaction.guild.get_role(admin_role_id)
    if admin_role in interaction.user.roles:
        global channel_id
        channel_id = channel.id
        guild_id = interaction.guild.id
        sqlite_func.set_channel_id(guild_id, channel_id)
        await interaction.response.send_message(f"Voice channel set to {channel.mention}", ephemeral=True)
    else:
        await interaction.response.send_message(f"You do not have permission to use this command", ephemeral=True)

@bot.slash_command(name="set_admin_role", description="Set the admin role so only admins can use commands")
async def set_channel(interaction: nextcord.Interaction, role: nextcord.Role):
    guild_id = interaction.guild.id
    sqlite_func.add_guild_if_not_exists(guild_id)
    admin_role_id = sqlite_func.get_role_id(guild_id)

    if admin_role_id is None or interaction.guild.get_role(admin_role_id) in interaction.user.roles:
        admin_input_role = role.id
        sqlite_func.set_role_id(guild_id, admin_input_role)
        await interaction.response.send_message(f"Admin role set to {role.name}", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
    
    
@bot.slash_command(name="setup", description="Run the setup for the bot")
async def setup(interaction: nextcord.Interaction, enable_command_creation: bool, enable_voice_creation: bool):
    #VC true/false
    #CMD true/false
    guild_id = interaction.guild.id
    admin_role_id = sqlite_func.get_role_id(guild_id)
    admin_role = interaction.guild.get_role(admin_role_id)
    
    if admin_role in interaction.user.roles:
        global global_enable_voice_creation 
        global_enable_voice_creation = enable_voice_creation
        global global_enable_command_creation
        global_enable_command_creation = enable_command_creation
        embed = nextcord.Embed(title="Setup reusults", 
                            description=f"enable_command_creation set to {global_enable_command_creation}\nenable_voice_creation set to {global_enable_voice_creation}", 
                            color=nextcord.Color.from_rgb(functions.random_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(content=f"You do not have permission to use this command", ephemeral=True)

@bot.slash_command(name="create_voice", description="Create a temporary voice channel")
async def create_voice(interaction: nextcord.Interaction):
    guild_id = interaction.guild.id
    admin_role_id = sqlite_func.get_role_id(guild_id)
    admin_role = interaction.guild.get_role(admin_role_id)
    
    if admin_role in interaction.user.roles:
        guild = interaction.guild
        channel_id = sqlite_func.get_channel_id(guild.id)
        category = bot.get_channel(channel_id).category
        new_channel = await guild.create_voice_channel(f"{interaction.user.name}'s channel", category=category)
        new_timer = asyncio.create_task(delete_channel_after(new_channel, interaction.user, 30))
        print(f"{interaction.user.name} has created the voice channel, {new_channel.id} at {functions.gettime()}")
        await interaction.response.send_message(f"Temporary voice channel {new_channel.mention} channel created.", ephemeral=True)
    else:
        await interaction.response.send_message(content=f"You do not have permission to use this command", ephemeral=True)
    
@bot.slash_command(name="delete_voice", description="Delete a voice channel, USE ONLY IF SOMETHING HAS BROKEN")
async def delete_voice(interaction: nextcord.Interaction, channel: nextcord.VoiceChannel):
    guild_id = interaction.guild.id
    admin_role_id = sqlite_func.get_role_id(guild_id)
    admin_role = interaction.guild.get_role(admin_role_id)
    
    if admin_role in interaction.user.roles:
        await channel.delete()
        await interaction.response.send_message(content=f"{channel.name} deleted", ephemeral=True)
        print(f"{channel.name} deleted at {functions.gettime()}")
    else:
        await interaction.response.send_message(content=f"You do not have permission to use this command", ephemeral=True)



@bot.event
async def on_voice_state_update(member, before, after):
    if global_enable_voice_creation == True:
        if after.channel is not None:  # Check if the member connected to a voice channel
            guild_id = after.channel.guild.id
            channel_id = sqlite_func.get_channel_id(guild_id)
            if after.channel.id == channel_id:  # Replace with the ID of your specific channel
                # Do something when a member joins the specific voice channel
                guild = after.channel.guild
                new_channel = await guild.create_voice_channel(f"{member.name}'s channel", category=after.channel.category)
                await member.move_to(new_channel)
                print(f"{member.name} has joined the voice channel, creating {new_channel.id} at {functions.gettime()}")
                if member in member_channels:  # If the member already has a channel and timer
                    old_channel, old_timer = member_channels[member]
                    old_timer.cancel()  # Cancel the old timer
                    if len(old_channel.members) == 0:  # If no one is in the old channel
                        await old_channel.delete()  # Delete the old channel
                # Start a new timer
                new_timer = asyncio.create_task(delete_channel_after(new_channel, member, 30))
                member_channels[member] = new_channel, new_timer

async def delete_channel_after(channel, member, delay):
    await asyncio.sleep(delay)  # Wait for the delay
    if len(channel.members) == 0:  # If no one is in the channel
        print(f"Deleting channel {channel.name} at {functions.gettime()}")  # Print the name of the channel that is being deleted
        await channel.delete()  # Delete the channel
    if member in member_channels:  # Check if the member is in the dictionary
        del member_channels[member]  # Remove the member from the dictionary
    
    
bot.run('TOKEN-HERE')