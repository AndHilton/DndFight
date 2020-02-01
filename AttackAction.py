"""
weapon and attacks for dnd simulator
"""
from collections import namedtuple

import DndDice as DnD
from AbilityScores import modStr

DamageTypes = sorted(['piercing','slashing','bludeoning','force','fire','poison','acid','cold','lightning','radiant'])

class AttackAction():
  """
  combining damage dice and modifier together into one thing, also nice things like description
  """

  def __init__(self, name, dice, modifiers, dmgType):
    self.name = name
    self.attackMod = modifiers[0]
    self.damageDice = dice
    self.damageMod = modifiers[1]
    self.damageType = dmgType

  def __str__(self):
    return f"{self.name} ({modStr(self.attackMod)} / {self.damageDice}{modStr(self.damageMod)})"

  def __repr__(self):
    return self.name


  def rollAttack(self,advantage='none'):
    """
    rolls an attack with the appropriate advantage
    """
    atk = DnD.rollD20(advantage)

    if atk == DnD.CRITICAL_SUCCESS:
      isCrit = True
    else:
      isCrit = False
    return DnD.AttackRoll(atk+self.attackMod, isCrit)

  def rollDamage(self, isCritical=False, critical=DnD.default_critical):
    """
    performs a damage roll and adds modifiers
    """
    if isCritical:
      base = critical(self.damageDice)
    else:
      base = self.damageDice.roll() + self.damageMod
    return base + self.damageMod

# Helper Functions

def attackFromString(string):
  """
  takes a string as input and returns an AttackAction
  """
  fields = string.split(',')
  name = fields[0]
  dice = DnD.diceFromString(fields[2])
  modifiers = (int(fields[1]),(int(fields[3])))
  dmgType = fields[4]
  return AttackAction(name,dice,modifiers,dmgType)

Fist = AttackAction('fist', DnD.Dice(1,4), (3,2), 'bludgeoning')
