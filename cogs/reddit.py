import discord
from discord.ext import commands
from discord import app_commands

import asyncpraw
import os
import random

class Reddit(commands.Cog):
  def __init__(self, bot) -> None:
    self.bot = bot 
    self.reddit = asyncpraw.Reddit(
      client_id = os.getenv("REDDIT_CLIENT"),
      client_secret = os.getenv("REDDIT_SECRET"),
      user_agent = os.getenv("REDDIT_USER_AGENT"),
    )

  @app_commands.command(name="cat", description="Get a cat pic!")
  async def cat(self, interaction: discord.Interaction) -> None:
    subreddit = await self.reddit.subreddit("cats")
    results = subreddit.search("flair:Cat Picture", 'new')

    submissions = []

    async for submission in results:
      if not "gallery" in submission.url:
        submissions.append(submission)

    chosen = random.choice(submissions)
    await interaction.response.defer()
    await interaction.followup.send(chosen.url)

  @app_commands.command(name="art", description="Get art from Epic Seven subreddit!")
  async def art(self, interaction: discord.Interaction) -> None:
    subreddit = await self.reddit.subreddit("EpicSeven")
    results = subreddit.search("flair:Art", 'new')

    submissions = []

    async for submission in results:
      if not "gallery" in submission.url:
        submissions.append(submission)

    chosen = random.choice(submissions)
    await interaction.response.defer()
    await interaction.followup.send(chosen.url)

  @app_commands.command(name="gorilla", description="Gorilla.")
  async def gorilla(self, interaction: discord.Interaction) -> None:
    subreddit = await self.reddit.subreddit("GorillaReddit")
    results = subreddit.search('new')

    submissions = []

    async for submission in results:
      if not "gallery" in submission.url:
        submissions.append(submission)

    chosen = random.choice(submissions)
    await interaction.response.defer()
    await interaction.followup.send(chosen.url)

async def setup(bot) -> None:
  await bot.add_cog(Reddit(bot))