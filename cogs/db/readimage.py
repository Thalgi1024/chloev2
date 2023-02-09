from PIL import Image

import requests
import pytesseract

def readDataFromImage(url):
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

  # Process text from image
  text = pytesseract.image_to_string(im1)
  lines = text.split('\n')
  print(lines)

  # Set up stat values
  Name = ""
  Attack = 0
  Defense = 0
  Health = 0
  Speed = 0
  CChance = 0
  CDamage = 0
  Effectiveness = 0
  EffectResist = 0

  #print(Name, Attack, Defense, Health, Speed, CChance, CDamage, Effectiveness, EffectResist)

  return Name, Attack, Defense, Health, Speed, CChance, CDamage, Effectiveness, EffectResist