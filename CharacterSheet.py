"""
handles information related to player character sheets
"""

from collections import deque

from Dnd_Dice import Dice
import AbilityScores as scores
from AbilityScores import AbilityIds, AbilityScores
from AttackAction import attackFromString
from PlayerCharacter import PlayerCharacter

dataKeys = ['name', 'race', 'alignment', 'level', 'class', 'hit-dice', 'hp', 'ac', 'ability-scores', 'attacks']

def readCharacterSheet(filename):
  with open(filename,'r') as f:
    dataLines = f.readlines()
  assert 'player-character' in dataLines[0], "file is invalid format"
  data = [ line.strip().split(':') for line in dataLines[1:] ]
  return parseCharacterData(data)


def parseCharacterData(dataList):
  dataQ = deque(dataList)
  dataDict = {}
  while len(dataQ) > 0:
    key, values = [ val.strip() for val in dataQ.popleft() ]
    if key in dataKeys:
      if key in ['name','race','alignment']:
        dataDict[key] = values
      elif key in ['hp','ac','level']:
        dataDict[key] = int(values)
      elif key in ['class','hit-dice']:
          # figure this out later
        dataDict[key] = values
      elif key == 'ability-scores':
        abDict = {}
        for i in range(len(scores.AbilityIds)):
          ability, score = [ val.strip() for val in dataQ.popleft() ]
          if ability in scores.AbilityIds:
            abDict[ability] = int(score)
          else:
            print(f'unrecognized ability {ability}')
        dataDict['ability-scores'] = AbilityScores(*[abDict[aId] for aId in scores.AbilityIds])
      elif key == 'attacks':
        num = int(values)
        attackList = []
        while num > 0:
          attack = dataQ.popleft()[0]
          num -= 1
          attackList.append(attackFromString(attack))
          dataDict['attacks'] = attackList
    else:
      print(f"skipping unrecognized key {key}")
  return dataDict

def generateCharacterStatBlock(charData):
  availableKeys = set(charData.keys)
  necessaryKeys = set(['name','level','hp','ac','ability-scores','attacks'])
  assert necesessaryKeys in availableKeys, "don't have necessary character data"
  pcStats = PlayerCharacter(charData['name'],charData['level'],charData['hp'],charData['ac'],charData['ability-scores'])
  for attack in charData['attacks']:
    pcStats.addAttackAction(attack)
  return pcStats  
