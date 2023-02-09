import discord
from discord.ext import commands

token = "MTA3MjY1ODgzNTMyOTc4NTg4Ng.G-9hNe.oLnuH3CIBxqRoZVEu-YkFCpb5tWsvRErt5DZ8E"

class ChloeBot(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix = "?", intents = discord.Intents.all())

  async def setup_hook(self):
    await self.load_extension(f"cogs.utils")
    await self.load_extension(f"cogs.misc")
    await self.load_extension(f"cogs.builds")
    await self.load_extension(f"cogs.roles")

    await bot.tree.sync()

  async def on_ready(self):
    print("Bot is online")

bot = ChloeBot()
bot.run(token)
