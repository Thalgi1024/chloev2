import discord
from discord.ext import commands
from discord import app_commands

class Utils(commands.Cog):
  def __init__(self, bot) -> None:
    self.bot = bot

  # Welcome message for JTFN
  @commands.Cog.listener()
  async def on_member_join(self, member):
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

  @app_commands.command(name="ping", description="Pings the bot.")
  async def ping(self, interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")

async def setup(bot) -> None:
  await bot.add_cog(Utils(bot))