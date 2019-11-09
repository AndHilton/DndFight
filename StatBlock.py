"""
classes, data types, and functions to represent creatures and characters
"""

from collections import namedtuple

import Dnd_Dice as DnD
from Dnd_Dice import Dice
from AttackAction import AttackAction
import AbilityScores as scores
from AbilityScores import Ability, AbilityIds, AbilityScores


class StatBlock():
  """
  the base class for representing creatures and characters
  encapsulates stats and metadata
  """

  speed = None
  attacks = []
  hitDice = []

  def __init__ (self, name, hp, ac, abilities):
    self.name = name
    self.maxHp = hp
    self.hp = hp
    self.ac = ac
    # take the input AbilityScore tuple and turn it into a mapping of ability to score,modifier
    self.abilities = {}
    abilityScores = scores.assignScores(abilities)
    for i in range(len(abilities)):
      self.abilities[AbilityIds[i]] = abilityScores[i]

  def __str__(self):
    # construct the header
    lines = [f"{self.name}",
             f"  HP : {self.hp}/{self.maxHp}, AC : {self.ac}",
             f"  Stats -"]
    # add the ability scores
    for val in AbilityIds:
      lines.append(f"    {val} : {self.abilities[val]}")
    # if we have a speed add it
    if self.speed:
      lines.append(f"  Speed : {self.speed}")

    # construct the actual return string
    ret_string = ""
    for line in lines:
      ret_string += f"{line}\n"
    return ret_string

  def setSpeed(self,speed):
    if speed > 0:
      self.speed = speed
    else:
      self.speed = 0

  def addHitDice(self,hitDice):
    self.hitDice.append(hitDice)

  def addAttack(self, name, atkMod, dmgDice, dmgMod, dmgType, bonus=(0,0)):
    mods = atkMod,dmgMod
    attack = AttackAction(name, dmgDice, mods, dmgType)
    self.addAttackAction(attack)
    
  def addAttackAction(self,attack):
    self.attacks.append(attack)

  def scores(self):
    return AbilityScores(*self.abilities.values())

  def isDead(self):
    return self.hp <= 0

  def damage(self, damage, dmgType=None):
    if not dmgType:
      self.hp -= damage

  def setAttack(self,index=0):
    try:
      self.currentAttack = self.attacks[index]
    except IndexError:
      raise ValueError("Not a valid attack")

  def makeAttack(self, target, attack=self.currentAttack):
    try:
      targetAc = target.ac
      isCrit, attackRoll = attack.rollAttack()
      if attackRoll >= targetAc:
        target.damage(attack.rollDamage(isCrit))
        return True
      else:
        return False
    except AttributeError:
      raise ValueError("Invalid Attack Target: no AC")
    except IndexError:
      raise IndexError(f"No Attack at index {index}")



base_statblock = StatBlock('Guy', 15, 12, [10,10,10,10,10,10])

ZennaraStats = StatBlock('Zennara', 51, 20, AbilityScores(17,10,15,8,8,16))
ZennaraStats.setSpeed(40)
#ZennaraStats.addAttack("Brother's Spear", 7, Dice(1,6), 5,'piercing', (1,2))
