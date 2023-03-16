import discord
from discord.ext import commands
from discord import app_commands

from .db import db
from .db import query
from .db import readimage

class Builds(commands.Cog):
  def __init__(self, bot) -> None:
    self.bot = bot

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, event):
    # Check if reaction is in pending builds channel
    if event.channel_id == 1072746656178655242:
      id_list = db.fetch(query.PENDING_BUILD_MESSAGE_ID_QUERY)
      
      for id in id_list:
        if id[0] == event.message_id:
          # Get info from database of build
          data = db.fetch(query.PENDING_BUILD_QUERY, id[0])
          print(data)

          # Remove from pending builds
          db.execute(query.PENDING_BUILD_DELETE_BY_ID, id[0])

          if len(data[0]) < 10:
            break

          values = data[0]

          # Add pending build to database
          id = db.fetch(query.BUILD_MAX_ID)[0][0] + 1 # Get newest ID
          db.execute(query.BUILD_INSERT, id, values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10])
          break

  @app_commands.command(name="requestaddbuild", description="Request to add a build to the database. Sets should be separated by commas with no spaces.")
  async def requestaddbuild(self, interaction: discord.Interaction, imageurl: str, name: str, sets: str) -> None:
    # Check to make sure inputs are valid
    validSets = [
      'speed', 
      'hit', 
      'crit', 
      'attack', 
      'health', 
      'defense', 
      'resist', 
      'destruction', 
      'lifesteal', 
      'immunity', 
      'counter', 
      'rage', 
      'unity', 
      'revenge', 
      'injury', 
      'penetration'
    ]

    # Check sets to make sure sets are valid
    setTokens = sets.lower().split(',')
    for s in setTokens:
      if not s in validSets:
        await interaction.response.send_message(f"Could not recognize set {s}. Make sure there are no whitespaces!")
        return

    # Check to make sure character name is valid
    alias = name.lower()
    charName = db.fetch(query.BUILD_NAME_QUERY, alias)

    if len(charName) < 1:
      await interaction.response.send_message(f"Could not recognize the character {name}. Your character may not be included in database yet!")
      return

    # Read stats from image
    attack, defense, health, speed, cchance, cdamage, effectiveness, effectresist = readimage.readDataFromImage(imageurl)

    # Send message to approval channel
    channel = self.bot.get_channel(1072746656178655242)
    message = await channel.send(imageurl)

    # Add to pending builds table
    db.execute(query.PENDING_BUILD_INSERT, message.id, charName[0][0], imageurl, sets, attack, defense, health, speed, cchance, cdamage, effectiveness, effectresist)

    await interaction.response.send_message("Request sent!")

  @app_commands.command(name="build", description="Query for a build from the database. Sets should be separated by commas with no spaces.")
  async def build(self, interaction: discord.Interaction, name: str, sets: str = "", minspeed: int = 0, maxspeed: int = 99999):
    # Match name with alias
    foundName = db.fetch(query.BUILD_NAME_QUERY, name.lower())

    if len(foundName) == 0:
      await interaction.response.send_message(f"No character with name {name} found!")
      return

    parameters = [foundName[0][0], minspeed, maxspeed]
    # Create query for build
    buildquery = query.BUILD_BASE_QUERY

    if sets != "":
      setList = sets.split(',')

      for set in setList:
        parameters.append(f"%{set}%")
        buildquery += query.BUILD_SET_QUERY

    buildquery += query.BUILD_END_QUERY
    
    # Execute query, respond with results
    builds = db.fetchWithTuple(buildquery, tuple(parameters))

    if len(builds) == 0:
      await interaction.response.send_message("No builds in database with matching parameters.")  

    for build in builds:
      await interaction.response.send_message(build[0])

async def setup(bot) -> None:
  await bot.add_cog(Builds(bot))