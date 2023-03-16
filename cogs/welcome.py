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

    data = db.fetch(query.WELCOME_CHANNEL_QUERY, str(guild_id))
    print(data)

    if member.guild.id != 524067267730735107:
      return

    channel = self.bot.get_channel(775185721182388275)

    embed = discord.Embed(
      title = "Welcome to JTFNS!",
      description = f"Welcome {member.mention}! Please make sure the read the rules, check out the role selection channel to select roles and gain access to the rest of the channels in the server!"
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