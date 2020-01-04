"""
Class representations of units used in encounter simulation
"""
import sys
import random as rand
from copy import *

from StatBlock import StatBlock

class SimUnit(StatBlock):
  """
  Wrapper around the StatBlock to aid in statistic collection
  """
  def __init__(self, stats, team):
    self.name = stats.name
    self.maxHp = stats.maxHp
    self.hp = stats.hp
    self.ac = stats.ac
    self.speed = stats.speed
    self.attacks = stats.attacks
    self.abilities = stats.abilities
    self.initiative = None
    self.team = team
    self.enemies = []
    self.target = None

  def __copy__(self):
    return SimUnit(copy(self.getStats()),self.team)
  
  def getStats(self):
    currentStats = StatBlock(self.name,
                             self.maxHp,
                             self.ac,
                             self.getAbilityScores())
    currentStats.hp = self.hp
    return currentStats

      
  def rollInitiative(self):
    if not self.initiative:
      self.initiative = self.abilityCheck("dex")
    return self.initiative

  def makeTurn(self):
    return self.getAttack()
  
  def getTarget(self):
    if not self.target:
      self.chooseTarget()
    return self.target

  def chooseTarget(self):
    # randomly
    try:
      self.target = rand.choice(self.enemies)
    except IndexError:
      self.target = None
    return self.target


  def addEnemies(self, *enemies):
    self.enemies.extend(enemies)

  def removeEnemy(self, enemy):
    self.enemies.remove(enemy)
    
                                
if __name__ == "__main__":

  from CharacterSheet import playerCharacterFromFile

  
  
  def setup():
    dummyCharacter = "data/og_monk"
    dummyStats = playerCharacterFromFile(dummyCharacter)
    dummy = SimUnit(dummyStats, "team")
    return dummyCharacter, dummyStats, dummy

  test = iter(setup())
  dummyCharacter = next(test)
  dummyStats = next(test)
  dummy = next(test)
  dummy2 = deepcopy(dummy)
  dummy.name = "dummy2"
  dummy.addEnemies(dummy2)
  dummyList = []
  for x in range(10):
    dummyx = copy(dummy)
    dummyList = dummyx.name = f"dummyx{x*1000}"
  dummy.addEnemies(dummyList)
  
  
