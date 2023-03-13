# File to run quick scripts for maintenance

import cogs.db.db as db
import cogs.db.readimage as readimage

#names = [
#
#]

#for nick, name in names:
#  query = "INSERT INTO Names VALUES (?, ?)"
 # db.execute(query, nick, name)

readimage.readDataFromImage("https://cdn.discordapp.com/attachments/1072673382694400051/1073342448153141318/unknown.png")