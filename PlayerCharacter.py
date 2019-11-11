"""
classes and functions to represent player character stats
"""

from DndDice import Dice
from AttackAction import AttackAction
from StatBlock import StatBlock
from AbilityScores import *  

def classHitDice(num, val):
  return lambda : Dice(num,val)

ClassToHitDice = { 'barbarian' : classHitDice(1,12),
                   'bard'      : classHitDice(1, 8),
                   'cleric'    : classHitDice(1, 8),
                   'druid'     : classHitDice(1, 8),
                   'fighter'   : classHitDice(1,10),
                   'monk'      : classHitDice(1, 8),
                   'paladin'   : classHitDice(1,10),
                   'ranger'    : classHitDice(1,10),
                   'rogue'     : classHitDice(1, 8),
                   'sorcerer'  : classHitDice(1, 6),
                   'warlock'   : classHitDice(1, 8),
                   'wizard'    : classHitDice(1, 6) }

class PlayerCharacter(StatBlock):
  """
  an extension of the StatBlock, represents a player character
    - hp - max and current
    - ac
    - ability scores and modifiers
    - attack actions
    - hit dice
    - class
    - level
  """

  def __init__ (self, name, level, hp, ac, abilityScores):
    super().__init__(name,hp,ac,abilityScores)
    self.level = level
    self.proficiency = proficiencyBonus(level)
    self.classLevels = { }
    self.hitDice = [ ]

  def addHitDice(self,hitDice):
    """
    adds hit dice
    """
    self.hitDice.append(hitDice)
    self.hitDice.sort(key=lambda x: x.value)

  def addClassLevel(self, classname):
    self.level += 1
    self.proficiency = proficiencyBonus(self.level)
    if classname in self.classLevels:
      self.classLevels[classname] += 1
    else:
      self.classLevels[classname] = 1
    addHitDice(ClassToHitDice[classname]())

def proficiencyBonus(level):
  return (level - 1) // 4 + 2