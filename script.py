# File to run quick scripts for maintenance

import cogs.db.db as db
import cogs.db.readimage as readimage

#names = [
#
#]

#for nick, name in names:
#  query = "INSERT INTO Names VALUES (?, ?)"
 # db.execute(query, nick, name)

readimage.readDataFromImage("https://media.discordapp.net/attachments/1007438571126399016/1007441693659906048/IMG_4573.png?width=1422&height=1066")