import discord
from discord.ext import commands
from discord import app_commands

from .db import db
from .db import query

class Welcome(commands.Cog):
  def __init__(self, bot) -> None:
    self.bot = bot

  # Welcome message for JTFN
  @commands.Cog.listener()
  async def on_member_join(self, member):
    guild_id = member.guild.id

    # Fetch information from database
    data = db.fetch(query.WELCOME_CHANNEL_QUERY, str(guild_id))

    if len(data) < 1:
      return

    channel_id = data[0][0]
    message = data[0][1]
    imagelink = data[0][2]

    channel = self.bot.get_channel(channel_id)

    embed = discord.Embed(
      title = "Welcome!",
      description = f"Welcome {member.mention}! {message}"
    )

    if not member.avatar == None:
      member_pfp = member.avatar.url
      embed.set_thumbnail(url = member_pfp)

    await channel.send(f"Welcome {member.mention}!")
    await channel.send(embed = embed)

  @app_commands.command(name="setwelcomechannel", description="Set a welcome channel for bot generated welcome messages")
  async def setwelcomechannel(self, interaction: discord.Interaction, channel_id: str, message: str = "", imagelink: str = ""):
    guild_id = interaction.guild_id

    # Update database for welcome channel
    db.execute(query.WELCOME_INSERT_CHANNEL, guild_id, channel_id, message, imagelink)
    db.execute(query.WELCOME_UPDATE_CHANNEL, channel_id, guild_id)
    db.execute(query.WELCOME_UPDATE_MESSAGE, message, guild_id)
    db.execute(query.WELCOME_UPDATE_IMAGE, imagelink, guild_id)

    await interaction.response.send_message("Updated welcome channel for server!")

async def setup(bot) -> None:
  await bot.add_cog(Welcome(bot))