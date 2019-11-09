"""
weapon and attacks for dnd simulator
"""
from collections import namedtuple

import Dnd_Dice as DnD
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

  def rollAttack(self):
    atk = D20.roll()
    if atk == 20:
      isCrit = True
    else:
      isCrit = False
    return DnD.AttackRoll(atk+self.attackMod, isCrit)

  def rollDamage(self, isCritical=False, critical=DnD.default_critical):
    if isCritical:
      base = critical(self.dice)
    else:
      base = self.damageDice.roll() + self.damageMod
    return base + self.damageMod


def attackFromString(string):
  fields = string.split(',')
  name = fields[0]
  dice = DnD.diceFromString(fields[2])
  modifiers = (int(fields[1]),(int(fields[3])))
  dmgType = fields[4]
  return AttackAction(name,dice,modifiers,dmgType)

# TODO change this to an item
class WeaponAttack(AttackAction):
  
  description = ""

  def addDescription(self, description):
    self.description.append(description)

  def enchant(self, level):
    self.isMagic = True
    self.level = level
    self.attackMod += level
    self.damageMod += level
    self.description.append(f" level-{level} magic weapon")