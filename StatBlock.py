"""
classes, data types, and functions to represent creatures and characters
"""

from collections import namedtuple

import DndDice as DnD
from AttackAction import AttackAction, Fist
import AbilityScores as scores
from AbilityScores import Ability, AbilityIds, AbilityScores


class StatBlock():
  """
  the base class for representing creatures and characters
  encapsulates stats and metadata
  """

  def __init__ (self, name, hp, ac, abilities):
    self.name = name
    self.maxHp = hp
    self.hp = hp
    self.ac = ac
    self.speed = None
    self.attacks = []
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

  def reset(self):
    self.hp = self.maxHp
    if len(self.attacks) > 0:
      self.setAttack()

  # methods for managing character stats

  def scores(self):
    """
    returns a tuple containing the characters ability scores
    """
    return AbilityScores(*self.abilities.values())

  def getAbilityScores(self):
    return [ ability.score for ability in self.scores() ]

  def isDead(self):
    """
    checks to see if the character is at 0 hp
    """
    return self.hp <= 0

  def setSpeed(self,speed):
    """
    sets the character speed value
    """
    if speed > 0:
      self.speed = speed
    else:
      self.speed = 0

  def addAttack(self, name, atkMod, dmgDice, dmgMod, dmgType, bonus=(0,0)):
    """
    adds an AttackAction of the given parameters to the characters available attacks
    """
    mods = atkMod,dmgMod
    attack = AttackAction(name, dmgDice, mods, dmgType)
    self.addAttackAction(attack)
    
  def addAttackAction(self,attack):
    """
    takes an AttackAction and adds it to available attacks
    """
    self.attacks.append(attack)

  def setAttack(self,index=0):
    """
    sets the characters primary attack action
    """
    try:
      self.currentAttack = self.attacks[index]
    except IndexError:
      raise ValueError("Not a valid attack")

  def getAttack(self,index=0):
      try:
        return self.attacks[index]
      except IndexError:
        raise ValueError("Not a valid attack")

  # methods for performing combat actions

  def abilityCheck(self, ability, advantage='none'):
    base = DnD.rollD20(advantage)
    try:
      return self.abilities[ability] + base
    except KeyError:
      raise ValueError(f"Invalid ability id {ability}")

  def damage(self, damage, dmgType=None):
    """
    records damage taken
    """
    if not dmgType:
      self.hp -= damage

  def makeAttack(self, target, attack=None, advantage='none'):
    """
    performs an attack on the given target
    """
    if attack is None:
      attack = self.currentAttack
    try:
      targetAc = target.ac
      attackRoll, isCrit = attack.rollAttack(advantage)
      if (attackRoll >= targetAc) or isCrit:
        target.damage(attack.rollDamage(isCrit))
        return True
      else:
        return False
    except Exception as exe:
      raise exe
    # except AttributeError:
    #   raise ValueError("Invalid Attack Target: no AC")
    # except IndexError:
    #   raise IndexError(f"No Attack at index {index}")


# some default test values

base_statblock = StatBlock('Guy', 15, 12, [10,10,10,10,10,10])
base_statblock.addAttackAction(Fist)

ZennaraStats = StatBlock('Zennara', 51, 20, AbilityScores(17,10,15,8,8,16))
ZennaraStats.setSpeed(40)
