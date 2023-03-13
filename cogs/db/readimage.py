from PIL import Image

import requests
import pytesseract

def readDataFromImage(url):
  im1 = processImage(url)

  # Process text from image
  text = pytesseract.image_to_string(im1)
  lines = text.split('\n')

  # Set up stat values
  Attack = -1
  Defense = -1
  Health = -1
  Speed = -1
  CChance = -1
  CDamage = -1
  Effectiveness = -1
  EffectResist = -1

  # Go through lines and look for data
  for line in lines:
    #Remove any %
    line = line.replace("%", "")
    tokens = line.split(' ')
    
    # Read in data
    if tokens[0] == "Attack":
      try: 
        Attack = int(tokens[1])
      except:
        print("Could not read attack")
        Attack = -1
    if tokens[0] == "Defense":
      try: 
        Defense = int(tokens[1])
      except:
        print("Could not read defense")
        Defense = -1
    if tokens[0] == "Health":
      try: 
        Health = int(tokens[1])
      except:
        print("Could not read health")
        Health = -1
    if tokens[0] == "Speed":
      try: 
        Speed = int(tokens[1])
      except:
        print("Could not read speed")
        Speed = -1
    
    print(line)

  im1 = im1.save("out.png")

  #print(Name, Attack, Defense, Health, Speed, CChance, CDamage, Effectiveness, EffectResist)

  return Attack, Defense, Health, Speed, CChance, CDamage, Effectiveness, EffectResist

def processImage(url):
  # Process image
  im = Image.open(requests.get(url, stream=True).raw)
  width,height = im.size

  left = 0
  top = height / 10
  right = width / 4
  bottom = height

  im1 = im.crop((left, top, right, bottom))

  thresh = 65
  fn = lambda x : 255 if x > thresh else 0
  im1 = im1.convert('L').point(fn, mode='1')

  return im1

def cleanText(line):
  cleanTokens = []

  keywords = ['Attack', 'Defense', 'Health', 'Critical', 'Hit', 'Chance', 'Damage', 'Effectiveness', 'Effect', 'Resistance']

  for token in line:
    