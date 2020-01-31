#!/usr/local/bin/python3
"""
Dungeons and Dragons damage calculator

method 1: roll your damage dice twice, add modifiers
method 2: roll your damage dice once double the value, add modifiers
method 3: determine max damage value, roll damage dice once, add modifiers

dice rolls are represented by a tuple (num, value)
damage rolls are tuple (dice, modifier)
uses classes for fun
"""

# random for the randint function
import random as rand
#namedtuple because it works nice
from collections import namedtuple


VERBOSE = False

CRITICAL_SUCCESS = 20
CRITICAL_FAILURE = 1

def vPrint(string):
  if VERBOSE:
    print(string)

AttackRoll = namedtuple("AttackRoll",['result','isCrit'])

# TODO make the value required, number optional
class Dice(namedtuple('DamageDice',['num','value'])):
  """
  representing dice as number of dice to roll and the max value on the dice
  """

  def roll(self):
    total = 0
    for i in range(self.num):
      total += rand.randint(1,self.value)
    return total
  
  def average(self):
    return self.num * (sum(range(1,self.value+1)) // self.value)

  # making it a class so I can overwrite the str representation of the namedtuple class
  def __str__(self):
    return f"{self.num}d{self.value}"

# TODO @dataclass DiceBag
#       easy way to get the standard dice

D100 = Dice(1,100)
D20  = Dice(1,20)
D12  = Dice(1,12)
D10  = Dice(1,10)
D8   = Dice(1,8)
D6   = Dice(1,6)

ADVANTAGE    = 'advantage'
DISADVANTAGE = 'disadvantage'

def rollOnce(dice=D20):
  return dice.roll()

def rollAdvantage(dice=D20):
  return max(dice.roll(),dice.roll())

def rollDisadvantage(dice=D20):
  return min(dice.roll(),dice.roll())

def rollD20(advantage=None):
  if advantage is ADVANTAGE:
    base = rollAdvantage()
  elif advantage is DISADVANTAGE:
    base = rollDisadvantage()
  else:
    base = rollOnce()
  return base

def diceFromString(string):
  params = [int(val) for val in string.split('d')]
  return Dice(*params)

class Smite(Dice):
  """
  a subclass of damafe dice that can be created with a single number
  """

  def __init__(self,level,extraLevels=0):
    self.num = 2 + level + extraLevels
    self.value = 8


# pairing damage dice plus modifier
# this let's you keep track of a particular roll
DamageRoll = namedtuple("DamageRoll", ['dice','modifier'])


# some example weapons
longsword = Dice(1, 8)
shortsword = Dice(1, 6)
scimitar = Dice(1,6)
greatsword = Dice(2, 6)
greataxe = Dice(1, 12)


StatBlock = namedtuple("StatBlock", ['hp','ac'])

blackbear = StatBlock(19,11)


## Critical Hit formula

def critical_rollTwice(dice):
  """
  roll damage dice twice 
  args -
   dice     : the damage dice to roll
  """
  num,val = dice
  dice.num = 2 * num
  return dice.roll()

def critical_rollAndDouble(dice):
  """
  roll damage dice once, double the value
  args -
   dice     : the damage dice to roll
  """
  base = dice.roll()
  return (2 * base)

def critical_rollAndMax(dice):
  """
  roll damage dice once, add max value of damage dice
  args -
   dice      : the damage dice to roll
  """
  num,val = dice
  return dice.roll() + (num * val)


# you can change this value to change the default
default_critical = critical_rollAndDouble


## Damage Calcuation

# this looks more complicated than it is
# don't worry too much about it
# 
# damageRoll can be written like (weapon,modifier)
def rollDamage(dice, modifier, isCrit=False, critical=default_critical):
  """
  calculates damage of a given weapon and modifier
  args -
   weapon   : damage dice of the weapon
   modifier : the damage modifier

  optional -
   isCrit   : critical hit?
   critical : method of calculation
  """
  if isCrit:
    return critical(dice) + modifier
  else:
    return dice.roll() + modifier

# same as above but you give it a smite level and weapon
def rollSmiteDamage(level, weapon, modifier, isCrit=False, critical=default_critical):
  """
  calculates smite damage with weapon and modifier
  args -
   level    : level of the smite
   weapon   : damage dice of the weapon
   modifier : the damage modifier

  optional -
   isCrit   : critical hit?
   critical : method of calculation
  """
  smite = Smite(level)
  if isCrit:
    return critical(weapon) + critical(smite) + modifier
  else:
    return weapon.roll() + smite.roll() + modifier

