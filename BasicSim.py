"""
functions to define basic simulation trials
"""
from collections import deque

from DndDice import *


# Dice Rolling Simulations


def runTrialAvgCritical(n, weapon, modifier, critFunc):
  """
  simulates n number of crits calculating using the provided parameters and method
  args -
    n            : the number of trials to run
    weapons      : a DamageDice object
    modifierr    : the damage modifier to use (+/- modifier)
    critFunc     : the crit function to use when calculating the damage
  """

  total = 0
  for i in range(n):
    total += rollDamage(weapon, modifier, True, critical=critFunc)
  return total / n


def simulateFight(targetHp, targetAc, attackMod, damageDice, damageMod):
  """
  simulates a single fight:
    - roll for attack (d20 + attackMod)
    - if successful (higher than target AC) roll damage
    - repeat until HP is 0
  """
  attackDice = DamageDice(1, 20)
  totalAttacks = 0
  totalHits = 0
  while targetHp > 0:
    totalAttacks += 1
    roll = attackDice.roll()
    isCritical = roll == 20
    if (roll + attackMod) >= targetAc or isCritical:
      totalHits += 1
      targetHp -= rollDamage(damageDice, damageMod, isCritical)
  return (totalAttacks, totalHits)


def runTrialAvgNumHits(n, targetHp, targetAc, attackMod, damageDice, damageMod):
  """
  run n trials to determine the average number of attacks it would take to kill a given target
  """
  totalAttempts = 0
  totalHits = 0
  for i in range(n):
    attempts,success = simulateFight(targetHp, targetAc, attackMod, damageDice, damageMod)
    totalAttempts += attempts
    totalHits += success
  return (totalAttempts/n,totalHits/n)


def simulatedDuel(charA, charB, verbose=True):

  fightLog = print if verbose else lambda x : None
  # set their attacks to the default
  charA.reset()
  charB.reset()

  combatants = deque([charA, charB])
  winner = None
  loser = None

  roundNum = 0
  Done = False
  while not Done:
    current = combatants[0]
    opponent = combatants[1]
    fightLog(f"{current.name} attacks {opponent.name}")
    hit = current.makeAttack(opponent)
    if hit:
      fightLog("Hit!")
      if opponent.isDead():
        Done = True
        fightLog("Fatal Blow")
        winner = current
        loser = opponent
    else:
      fightLog("Miss!")
    combatants.rotate()
    roundNum += 1
  fightLog(f"{winner.name} is victorious")
  return winner
