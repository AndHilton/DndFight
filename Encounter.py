"""
Rethinking the structure of the Encounter Simulations
"""

# general pylib stuff
import sys
import random as rand
from collections import namedtuple
from itertools import count
from copy import copy

# DnD Fight modules
from StatBlock import StatBlock, base_statblock

DEBUG_LEVEL = 1

if DEBUG_LEVEL >= 1:
    fightLog = print
else:
    fightLog = lambda x : None

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

"""
NOTE
        --Layout--

Encounter : handles the highest level interactions
            - Initiative
            - Armies
            - Running the Simulation
            - End Condition
            - Eventually maybe a map too, why not

SimArmy : a collection of SimUnits, encapsulates a "side" of the encounter
          - collects all units on a side, alive and dead
          - handles the "objective" of a side (e.g. enemies)

InitiativeOrder : handles the order of SimUnits in a round
                  - sorted by the InitiativeScore of the Units
                  - Actively updated as the round progresses

SimUnit : an individual unit in combat, Encapsulates a StatBlock
          - includes the Unit stats and behavior
          - handles its own individual turn, and is in charge of its actions
          - defers to its team for objective (e.g. enemies)          
"""
        

class EncounterSim():
    """
    @brief controller class to handle running an encounter
    --- Relevant Stats ---
        - Number of Units
        - Number of Rounds
        - Winning Side :
            - Number of Survivors
            - Remaining HP
    """

    results = namedtuple("results", ['unitTotal', 'roundTotal', 'winner'])

    def __init__(self, *armies):
        # TODO
        # armies enemies have to be set before hand
        self.winner = None
        self.started = False
        self.initiative = InitiativeOrder()
        self.sides = armies
        self.initStats()

    def initStats(self):
        self.stats = { }
    
    def run(self):
        """
        # roll initiative
        # run rounds until done
        # collect results
        """
        self.rollInitiative()
        countRounds = count(1,1)
        # walrus? - while not (done := self.runRound()):
        while not self.isDone():
            self.rounds = next(countRounds)
            fightLog(f"round {self.rounds}")
            self.runRound()
            # TODO update stats
        fightLog("finished")
        return self.collectResults()


    def rollInitiative(self):
        """
        # take the list of all fighters, have them roll initiative
        """
        if not self.started:
            self.rounds = 0
            for army in self.sides:
                self.initiative.add(*army.getUnits())
            self.started = True

    def runRound(self):
        """
        # run a round of initiative
        """
        if self.started:
            done = False
            for unit in self.initiative:
                unit.survival = self.rounds
                slain = unit.takeTurn()
                self.initiative.remove(*slain)
            done = self.isDone()
            if done:
                self.declareWinner()
            return done
        else:
            raise Exception("must roll initiative first")

    def isDone(self):
        """
        all armies are done
        """
        return all([ army.isDone() for army in self.sides])

    def declareWinner(self):
        """
        declare the winner
        """
        self.winner = [ army for army in self.sides if army.survived() ].pop()
        return self.winner

    def collectResults(self):
        """
        TODO
        # collect relevant statistics
        """
        return self.stats

class SimArmy():
    """
    @brief collection of units and 'tactical' logic
    --- Relevant Stats ---
        - Total HP
        - Average HP
        - Average AC
        - Total Damage
        - Average Damage
        - Average Survival (in Rounds)
        - Total Attacks
        - Total Hits
        - Average Hit %
    """

    results = namedtuple("results", ['totalHP',
                                     'avgHp'
                                     'size',
                                     'avgAc',
                                     'totalDmg',
                                     'avgDmg',
                                     'avgSurvival',
                                     'totalAttacks',
                                     'totalHits',
                                     'avgHitRate'])

    def __init__(self, unitStats):
        self.units = set([ SimUnit(stats, self) for stats in unitStats ])
        self.grave = set( )
        self.opponents = set( )
        self.initStats()
    
    def initStats(self):
        """
        initialize the stats tracker
        """
        self.stats = { }

    def isDone(self):
        """        
        an army is done when there are no units left or if all of its opponents are done
        """
        haveUnits = bool(self.units)
        haveActiveEnemies = bool(self.getEnemies())
        return not (haveUnits and haveActiveEnemies)

    def addOpponents(self, *opponents):
        """
        adds the given enemy list
        """
        self.opponents |= set().union(opponents)
    
    def getUnits(self):
        """
        return active units
        """
        return self.units

    def getEnemies(self):
        """
        TODO
        return our enemies (the set of units from all of our opposing armies)
        """
        return list(set().union(*[army.getUnits() for army in self.opponents]))
        
    def moveToGrave(self, unit):
        """
        moves the given unit from the list of acitve units into the grave
        """
        self.units.discard(unit)
        self.grave.add(unit)

    def survived(self):
        """
        returns true if there are any units remaining
        """
        return bool(self.units)


class InitiativeOrder():
  """
  @brief container class handle Initiative Order of the Encounter  
  properties : iterable
  notes -
    ~ updates as units are added and removed
  """

  InitiativeEntry = namedtuple("InitiativeEntry", ["score", "unit"])

  def __init__(self, *unitList):
    self.order = list(unitList)
    self.current = iter(self.order)
    self.complete = False
    
  def __iter__(self):
    aCopy = copy(self)
    aCopy.top()
    return aCopy
  
  def __next__(self):
    return next(self.current)
  
  def update(self):
    def initiativeSortKey(unit):
      return unit.initiative()
    self.order.sort(key=initiativeSortKey, reverse=True)

  def top(self):
    self.update()
    self.current = iter(self.order)
    
  def add(self, *units):
    self.order.extend(units)
    self.update()

  def remove(self, *units):
    for unit in units:
        self.order.remove(unit)
    self.update()
    return units


class SimUnit(StatBlock):
    """
    @brief a single unit in the encounter, handles logic of "taking a turn"
    --- Relevant Stats ---
        - HP
        - AC
        - Initiative Order
        - Survival (in Rounds)
        - Number of Attacks
        - Number of Hits
        - Hit %
        - Average Damage / Hit
    """
    
    results = namedtuple("results", ['hp',
                                     'ac',
                                     'initiative',
                                     'survival',
                                     'attacks',
                                     'hits',
                                     'hitRate',
                                     'dmg'])

    def __init__(self, stats, team):
        self.name = stats.name
        self.maxHp = stats.maxHp
        self.hp = stats.hp
        self.ac = stats.ac
        self.speed = stats.speed
        self.attacks = stats.attacks
        self.abilities = stats.abilities
        self.team = team
        self.survival = 0
        self.initiativeScore = None
        self.target = None
        self.currentAttack = stats.getAttack()
        self.initStats()
    
    def initStats(self):
        """
        initialize the stats tracker
        """
        self.stats = { }

    def rollInitiative(self):
        """
        rolls initiative if it has not been set

        @return : the initiative score
        """
        self.initiativeScore = self.abilityCheck('dex')
        return self.initiativeScore

    def initiative(self):
        if not self.initiativeScore:
            self.rollInitiative()
        return self.initiativeScore

    def takeTurn(self):
        """
        attack your current target (select one if None)
        if they die, return them
        if we have mulit-attack go through 
        return a list of enemies we killed
        TODO factor in multiattack
        """
        if not self.target or self.target.isDead():
            self.selectTarget()
        slain = [ ]
        if self.target:
            target = self.target
            attackAction = self.getAttack()
            attackRoll = attackAction.rollAttack()
            if (attackRoll.isCrit) or (attackRoll.result >= self.target.ac):
                fightLog(f"{self.name} {'critical' if attackRoll.isCrit else ''} hit")
                dmg = attackAction.rollDamage(attackRoll.isCrit)
                isDead = self.__class__.dealDamage(self.target,dmg)
                if isDead:
                    slain.append(target)
                    self.target = None
        return slain
    
    def enemies(self):
        """
        right now our enemies are exactly our team's enemies
        """
        return self.team.getEnemies()

    def selectTarget(self):
        """
        right now randomly select from enemies()
        """
        try:
            self.target = rand.choice(self.enemies())
        except IndexError:
            self.target = None
        return self.target

    @staticmethod
    def dealDamage(target, damage):
        """
        deals damage to the target
        """
        if target:
            target.takeDamage(damage)
        return target.isDead()

    def takeDamage(self, damage):
        """
        reduce hp by amount of damage
        if we fall to 0 hp or below die()
        return True if fatal, False otherwise
        """
        fightLog(f"{self.name} took {damage} dmg")
        self.hp -= damage
        if self.hp <= 0:
            self.die()
            return True
        else:
            return False
        

    def die(self):
        """
        move yourself to your team's graveyard
        """
        fightLog(f"{self.name} has died")
        self.team.moveToGrave(self)


if __name__ == "__main__":
    dummyStats = base_statblock
    teamFoo = SimArmy([dummyStats for x in range(8)])
    teamBar = SimArmy([dummyStats for x in range(8)])
    teamFoo.addOpponents(teamBar)
    teamBar.addOpponents(teamFoo)
    sim = EncounterSim(teamFoo, teamBar)
    sim.run()