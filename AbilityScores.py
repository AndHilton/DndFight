"""
encapsulates ability scores, and modifiers
"""

from collections import namedtuple
from Dnd_Dice import D20

# the ability ids
AbilityIds = ( 'str', 'dex', 'con', 'wis', 'int', 'cha' )
# the skill ids

Skills = { 'acrobatics'      : 'dex',
           'animal handling' : 'wis',
           'arcana'          : 'int',
           'athletics'       : 'str',
           'deception'       : 'cha',
           'history'         : 'int',
           'insight'         : 'wis',
           'intimidiation'   : 'cha',
           'investigation'   : 'int',
           'medicine'        : 'wis',
           'nature'          : 'int',
           'perception'      : 'wis',
           'performance'     : 'cha',
           'persuasion'      : 'cha',
           'religion'        : 'int',
           'sleight of hand' : 'dex',
           'stealth'         : 'dex',
           'survival'        : 'wis' }


def scoreToModifier(score):
  """
  takes in an ability score value and returns the corresponding modifier
  """
  return (score - 10) // 2

def modStr(modifier):
  if modifier > 0:
    op = '+'
  else:
    op = ' '
  return f"{op}{modifier}"



class Ability():
  """
  combines score and modifier, with a nice string representation
  """
  def __init__(self,score):
    self.score = score
    self.modifier = scoreToModifier(score)

  def __str__(self):
    return f"({self.score}, {modStr(self.modifier)})"


# namedtuple for representing ability scores
AbilityScores = namedtuple("AbilityScores",AbilityIds)

def assignScores(scores):
  abilityList = []
  for score in scores:
    abilityList.append(Ability(score))
  return AbilityScores(*abilityList)


# the ability scores provided by the 'standard distribution' option
standard_score_distribution = [ 15, 14, 13, 12, 10, 8 ]

def assignStandardScores(abilityPriority):
  pass

downTheLine = assignScores(standard_score_distribution)
ability_scores_all_tens = assignScores([10 for ability in AbilityIds])