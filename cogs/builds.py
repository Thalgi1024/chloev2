import discord
from discord.ext import commands
from discord import app_commands

from .db import db

class Builds(commands.Cog):
  def __init__(self, bot) -> None:
    self.bot = bot

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, event):
    # Check if reaction is in pending builds channel
    if event.channel_id == 1072746656178655242:
      query = "SELECT message_id FROM PendingBuilds"
      id_list = db.fetch(query)
      
      for id in id_list:
        if id[0] == event.message_id:
          # Get info from database of build
          query = "SELECT CharacterName, ImageLink, Sets, Attack, Defense, Health, Speed, CChance, CDamage, Effectiveness, EffectResist FROM PendingBuilds WHERE message_id = ?"
          data = db.fetch(query, id[0])
          print(data)

          # Remove from pending builds
          query = "DELETE FROM PendingBuilds WHERE message_id = ?"
          db.execute(query, id[0])

          if len(data[0]) < 10:
            break

          values = data[0]

          # Add pending build to database
          query = "INSERT INTO Builds Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

          # Get newest ID
          idquery = "SELECT MAX(BuildID) FROM Builds"
          id = db.fetch(idquery)[0][0] + 1
          
          db.execute(query, id, values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10])
          break

  @app_commands.command(name="requestaddbuild", description="Request to add a build to the database. Sets should be separated by commas with no spaces.")
  async def requestaddbuild(self, interaction: discord.Interaction, name: str, imageurl: str, attack: int, defense: int, health: int, speed: int, cchance: float, cdamage: float, effectiveness: float, effectresist: float, sets: str) -> None:
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
    query = "SELECT DISTINCT name FROM Names WHERE alias = ?"
    charName = db.fetch(query, alias)

    if len(charName) < 1:
      await interaction.response.send_message(f"Could not recognize the character {name}. Your character may not be included in database yet!")
      return

    # Send message to approval channel
    channel = self.bot.get_channel(1072746656178655242)
    message = await channel.send(imageurl)

    # Add to pending builds table
    query = "INSERT INTO PendingBuilds VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    db.execute(query, message.id, charName[0][0], imageurl, sets, attack, defense, health, speed, cchance, cdamage, effectiveness, effectresist)

    await interaction.response.send_message("Request sent!")

  @app_commands.command(name="build", description="Query for a build from the database. Sets should be separated by commas with no spaces.")
  async def build(self, interaction: discord.Interaction, name: str, sets: str = "", minspeed: int = 0, maxspeed: int = 99999):
    # Match name with alias
    namequery = "SELECT name from Names WHERE alias = ?"
    foundName = db.fetch(namequery, name.lower())

    if len(foundName) == 0:
      await interaction.response.send_message(f"No character with name {name} found!")
      return

    # Create query for build
    buildquery = f"SELECT ImageLink FROM Builds WHERE CharacterName = \"{foundName[0][0]}\" AND Speed >= {minspeed} AND Speed <= {maxspeed} "

    if sets != "":
      setList = sets.split(',')

      for set in setList:
        buildquery += f"AND Sets LIKE \'%{set}%\' "

    buildquery += "ORDER BY RANDOM() LIMIT 3"
    print(buildquery)
    
    # Execute query, respond with results
    builds = db.fetch(buildquery)

    if len(builds) == 0:
      await interaction.response.send_message("No builds in database with matching parameters.")  

    for build in builds:
      await interaction.response.send_message(build[0])

async def setup(bot) -> None:
  await bot.add_cog(Builds(bot))