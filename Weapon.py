"""
module to represent weapon attacks
"""

class Weapon(AttackAction):

  description = ""

  def __init__(self, name, dice, ability, modifiers=(0,0), dmgType):
    self.abiltiyMod = ability
    super().__init__(name, dice, modifiers, dmgType)

  def addDescription(self, description):
    self.description.append(description)

  def enchant(self, level):
    self.isMagic = True
    self.level = level
    self.attackMod += level
    self.damageMod += level
    self.description.append(f" level-{level} magic weapon")