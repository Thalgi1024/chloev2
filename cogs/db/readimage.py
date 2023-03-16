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
    print(line)
    tokens = cleanText(line)
    print(tokens)
    
    if len(tokens) < 2:
      continue

    # Read in data
    if tokens[0] == "Attack":
      try: 
        Attack = int(tokens[1])
      except:
        print("Could not read attack")
    if tokens[0] == "Defense":
      try: 
        Defense = int(tokens[1])
      except:
        print("Could not read defense")
    if tokens[0] == "Health":
      try: 
        Health = int(tokens[1])
      except:
        print("Could not read health")
    if tokens[0] == "Speed":
      try: 
        Speed = int(tokens[1])
      except:
        print("Could not read speed")
    if tokens[0] == "Effectiveness":
      try: 
        Effectiveness = float(tokens[1])
      except:
        print("Could not read effectiveness")

    if len(tokens) < 3:
      continue

    if tokens[0] == "Effect":
      try: 
        EffectResist = float(tokens[2])
      except:
        print("Could not read effectresist")
        EffectResist = -1

    if len(tokens) < 4:
      continue

    if tokens[0] == "Critical" and tokens[2] == "Chance":
      try: 
        CChance = float(tokens[3])
      except:
        print("Could not read cchance")
        CChance = -1
    if tokens[0] == "Critical" and tokens[2] == "Damage":
      try: 
        CDamage = float(tokens[3])
      except:
        print("Could not read cdamage")
        CDamage = -1

  im1 = im1.save("out.png")

  print(Attack, Defense, Health, Speed, CChance, CDamage, Effectiveness, EffectResist)

  return Attack, Defense, Health, Speed, CChance, CDamage, Effectiveness, EffectResist

def processImage(url):
  # Process image
  im = Image.open(requests.get(url, stream=True).raw)
  width,height = im.size

  left = 0
  top = height / 10
  right = width / 3
  bottom = height

  im1 = im.crop((left, top, right, bottom))

  thresh = 65
  fn = lambda x : 255 if x > thresh else 0
  im1 = im1.convert('L').point(fn, mode='1')

  return im1

def cleanText(line):
  line = line.replace("%", "")
  tokens = line.split(' ')

  cleanTokens = []

  keywords = ['Attack', 'Defense', 'Health', 'Critical', 'Hit', 'Chance', 'Damage', 'Effectiveness', 'Effect', 'Resistance']

  for token in tokens:
    if token == None:
      continue

    cleanToken = removePunctuation(token)

    if len(cleanToken) > 0:
      cleanTokens.append(cleanToken)

  return cleanTokens

def removePunctuation(text):
  result = text
  punc = '''!()-[]{};:'"\,<>/?@#$%^&*_~°'''

  # Remove dots only after first dot, to keep decimal
  decimalFound = False

  # Check to see if token contains numeric characters. Remove dots for non-numeric tokens
  isNumeric = any(char.isdigit() for char in text)

  offset = 0

  for idx, c in enumerate(text):
    if c == '.':
      if decimalFound and isNumeric:
        result = result[:idx - offset] + result[idx - offset + 1:]
        offset += 1
      else:
        decimalFound = True

    if c in punc:
      result = result.replace(c, "")
      offset += 1

  return result
