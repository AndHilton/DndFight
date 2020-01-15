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

## TODO temporarily (?) moving everything to Encounter module while I 
#       reorganize structure of encounter simulation
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
    """
    TODO
    figure out a way to construct a "turn" as a collection of actions
    want to future proof this somewhat against extra-attack
    construct a series of closures?
    have a member called "action"
    """
    pass

  def getTarget(self):
    if not self.target:
      self.chooseTarget()
    return self.target

  def chooseTarget(self):
    # randomly
    try:
      self.target = rand.choice(team.enemies)
    except IndexError:
      self.target = None
    return self.target

  def addEnemies(self, *enemies):
    self.enemies.extend(enemies)

  def removeEnemy(self, enemy):
    self.enemies.remove(enemy)


class SimulationArmy():

  """
  Simulates a "side" of an encouter

  Members:
  list of alive members
  list of dead members
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
    self.enemies = []

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
    self.complete = False
    
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
    # get current enemy, maybe this happens internal to the sim unit
    # attack enemy
    # NOTE let each unit decide what their turn looks like,
    #  simulation just iterates until the unit determines it's turn is over
    # TODO future proof against multi-attack, other kinds of actions
    # TODO formalize removing a unit
    # update current side totals
    # enemy dead ? remove from initiative order
    pass
  done = false # TODO : is one side dead
  return done

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

# create data structs for stats/results

def simulateBasicEncounter(*armyStats):

  # take input of the sides (as StatBlocks),
  # create a list of simulation entities for each side

  # each entity should know what there enemies are

  # assign an initiative order randomly (1d20 + dex)

  # while not done...
  ## simulate one round
  ## done?
  
  # return StatsToCapture

  """
  TODO
  1 - initialize all sides, roll initiative
  2 - initalize return data
  3 - while encounter not done
  4 - run a single round of initiative
  """
  armies = [ SimulationArmy(stats) for stats in armyStats ]

  # initialize the armies
  #   - make sure they have all the appropriate enemies
  initiative = InitiativeOrder()
  # determine initiative order
  done = False
  while not done:
    done = simualateOneRound(initiative)
  # collect results
  results = None
  return results
  
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
  
