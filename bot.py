import discord
from discord import app_commands
from discord.ext import commands

# Aktiviere alle Intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
    # Synchronisiere Slash-Befehle
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    """This is a ping command"""
    await interaction.response.send_message('Pong!')

@bot.tree.command(name="kick")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    """This is a kick command"""
    await member.kick(reason=reason)
    await interaction.response.send_message(f'Kicked {member.mention}!')

@bot.tree.command(name="ban")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    """This is a ban command"""
    await member.ban(reason=reason)
    await interaction.response.send_message(f'Banned {member.mention}!')

@bot.tree.command(name="clear")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    """This is a clear command"""
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f'Cleared {amount} messages!', ephemeral=True)

@bot.tree.command(name="mute")
@app_commands.checks.has_permissions(moderate_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member):
    """This is a mute command"""
    await member.edit(mute=True)
    await interaction.response.send_message(f'Muted {member.mention}!')

@bot.tree.command(name="unmute")
@app_commands.checks.has_permissions(moderate_members=True)
async def unmute(interaction: discord.Interaction, member: discord.Member):
    """This is an unmute command"""
    await member.edit(mute=False)
    await interaction.response.send_message(f'Unmuted {member.mention}!')

@bot.tree.command(name="create_channel")
@app_commands.checks.has_permissions(manage_channels=True)
async def create_channel(interaction: discord.Interaction, name: str):
    """This is a create_channel command"""
    await interaction.guild.create_text_channel(name)
    await interaction.response.send_message(f'Created {name}!')

@bot.tree.command(name="delete_channel")
@app_commands.checks.has_permissions(manage_channels=True)
async def delete_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    """This is a delete_channel command"""
    await channel.delete()
    await interaction.response.send_message(f'Deleted {channel.name}!')

@bot.tree.command(name="add_role")
@app_commands.checks.has_permissions(manage_roles=True)
async def add_role(interaction: discord.Interaction, role: discord.Role, member: discord.Member):
    """This is an add_role command"""
    await member.add_roles(role)
    await interaction.response.send_message(f'Added {role.mention} to {member.mention}!')

@bot.tree.command(name="remove_role")
@app_commands.checks.has_permissions(manage_roles=True)
async def remove_role(interaction: discord.Interaction, role: discord.Role, member: discord.Member):
    """This is a remove_role command"""
    await member.remove_roles(role)
    await interaction.response.send_message(f'Removed {role.mention} from {member.mention}!')

@bot.tree.command(name="server_info")
async def server_info(interaction: discord.Interaction):
    """This is a server_info command"""
    guild = interaction.guild
    embed = discord.Embed(title=guild.name, description=guild.description or "No description", color=discord.Color.blue())
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(name='Members', value=guild.member_count, inline=True)
    embed.add_field(name='Channels', value=len(guild.channels), inline=True)
    embed.add_field(name='Roles', value=len(guild.roles), inline=True)
    
    if guild.owner:
        embed.add_field(name='Owner', value=guild.owner.mention, inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="user_info")
async def user_info(interaction: discord.Interaction, member: discord.Member = None):
    """This is a user_info command"""
    if member is None:
        member = interaction.user
    
    embed = discord.Embed(title=member.name, description=member.mention, color=discord.Color.blue())
    
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    
    roles = [role.mention for role in member.roles if role != interaction.guild.default_role]
    embed.add_field(name='Roles', value=', '.join(roles) if roles else 'No roles', inline=False)
    
    embed.add_field(name='Joined', value=member.joined_at.strftime('%d.%m.%Y'), inline=True)
    
    if member.premium_since:
        embed.add_field(name='Boosted', value=member.premium_since.strftime('%d.%m.%Y'), inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="say")
async def say(interaction: discord.Interaction, message: str):
    """This is a say command"""
    await interaction.response.send_message(message)


bot.run('MTEwODg3NTY0ODU4MTI0NzA1Nw.G7nY4g.Y7MwYJh1HFaP4lv1apCkkh6w9HRVbU0uN_w11M')