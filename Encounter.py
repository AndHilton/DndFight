"""
Simulating a combat encounter using StatBlocks
"""
import sys
from collections import *
from queue import PriorityQueue
from copy import copy

from StatBlock import StatBlock

VERBOSE = False
def logNone(string):
  pass

battleLog = logNone

def set_verbose(verbose=True):
  global VERBOSE
  global battleLog
  if verbose:
    VERBOSE = True
    battleLog = print
  else:
    VERBOSE = False
    battleLog = logNone
    

"""
* Encounter Statistics :

** Stats By Encounter :
*** - Number of Units
*** - Winning Side :
**** - Number of Survivors
**** - Remaining HP
*** - Number of Rounds

** Stats By Side :
*** - Total HP
*** - Average HP
*** - Average AC
*** - Total Damage
*** - Average Damage
*** - Average Survival (in Rounds)
*** - Total Attacks
*** - Total Hits
*** - Average Hit %

** Stats By Unit :
*** - HP
*** - AC
*** - Initiative Order
*** - Survival (in Rounds)
*** - Number of Attacks
*** - Number of Hits
*** - Hit %
*** - Average Damage / Hit
"""

class SimulationArmy():

  """
  Simulates a "side" of an encouter
  
  Members:
  list of alive members
  list of dead members

  -- Statistics --
  Before Encounter:
  - Number of Units
  - Total HP
  - Average HP
  - Average AC
  
  Stats to Track:
  - Total Damage
  - Running Average Damage/Round

  Summary Stats:
  - Average Survival
  - Total Attacks
  - Total Hits
  - Average Hit %
  """
  
  def __init__(self, statblocks):
    self.squad = [ SimUnit(stat) for stat in statblocks ]  # TODO : implement the SimUnit Class
    self.graveyard = []
    # before encounter
    self.size = len(statblocks)
    self.totalHP = sum([unit.hp for unit in statblocks]) # TODO : check unit api
    self.avgHP = self.totalHP / self.size
    self.avgAC = sum([unit.ac for unit in statblocks]) / self.size # TODO : check unit api
    self.currentDamage = 0

  def addEnemies(self, enemies):
    for unit in self.squad:
      unit.addEnemies(enemies)

      
InitiativeEntry = namedtuple("InitiativeEntry", ["score", "unit"])
END_INITIATIVE = InitiativeEntry(0, None)

class InitiativeOrder():

  """
  convenience class to encapsulate going through the order of inititiative
  
  basically a priority queue with the ability to update entries.
  
  need to be able to loop over each unit in the initiative order
  until the end of the order is reached

  need to be able to add units in an ordered way (higher initiatives come earlier)
  need to be able to remove units cleanly from the order
  """

  def __init__(self):
    self.order = []
    self.current = iter(self.order)
    
  def __iter__(self):
    aCopy = copy(self)
    aCopy.top()
    return aCopy
  
  def __next__(self):
    return next(self.current)
  
  def update(self):
    def sortKey(unit):
      return unit.initiative
    self.order.sort(key=sortKey, reverse=True)

  def top(self):
    self.update()
    self.current = iter(self.order)
    
  def add(self, unit):
    self.order.append(unit)
    self.update()

  def remove(self, unit):
    self.order.remove(unit)
    self.update()


def simualateOneRound(initiative):
  """
  goes through initiative order and simulates units actions
  """
  done = false
  for unit in initiative:
    unit.survival += 1
    # get side
    # get current enemy
    # attack enemy
    # update current side totals
    # enemy dead ? remove from initiative order
    pass
  done = false # TODO : is one side dead
  return done


def simulateBasicEncounter(*armyStats):

  # take input of the sides (as StatBlocks),
  # create a list of simulation entities for each side

  # each entity should know what there enemies are

  # assign an initiative order randomly (1d20 + dex)

  # while not done...
  ## simulate one round
  ## done?
  
  # return StatsToCapture
  pass


  
if __name__ == "__main__":
  set_verbose(True)
  import random

  class Dummy():

    def __init__(self, name, initiative):
      self.name = name
      self.initiative = initiative
      self.survival = 0

    def __str__(self):
      return f"hello i'm {self.name} at initiative {self.initiative}"

  
  def setup():
    foo = InitiativeOrder()
    names = [ f"name{n}" for n in range(20) ]
    scores = [ n for n in range(11,17) ]
    units = [ Dummy(name, random.choice(scores)) for name in names ]
    foo.order.append(Dummy("test",1))
    guy = units[4]
    guy.name = "guy"
    for dummy in units:
      foo.add(dummy)
    return foo, names, scores, units, guy

  foo, names, scores, dummies, guy = setup()
  
