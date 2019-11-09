"""
classes and functions to represent player character stats
"""

from Dnd_Dice import Dice
from AttackAction import AttackAction
from StatBlock import StatBlock
from AbilityScores import *  

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
    self.level = level
    super().__init__(name,hp,ac,abilityScores)


  def addClassLevel(self, classname):
    pass
