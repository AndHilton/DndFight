"""
unit tests for the encounter simulator
"""

import sys
import unittest as test
from random import choice
from mock import MagicMock, Mock

from Encounter import EncounterSim, SimArmy, InitiativeOrder, SimUnit
from StatBlock import StatBlock, base_statblock


class SimUnitTest(test.TestCase):

    def setUp(self):
        # mock setup
        self.mockTeam = MagicMock(spec=SimArmy)
        self.mockTarget = MagicMock(spec=SimUnit)

        self.statblock = base_statblock
        self.dummy = SimUnit(self.statblock, self.mockTeam)
    
    def test_initialization(self):
        """
        * a simunit is not its stat block
        * make sure the unit's team is the same as the mock
        * dummy has no initiative
        * 
        """
        self.assertIsNot(self.statblock, self.dummy)
        self.assertIs(self.mockTeam, self.dummy.team)
        self.assertIsNone(self.dummy.initiativeScore)

    def test_rollInitiative(self):
        self.assertIsNone(self.dummy.initiativeScore)
        initiative = self.dummy.rollInitiative()
        self.assertIs(type(initiative), int)
        self.assertEqual(initiative, self.dummy.initiative())
        # idempotent
        self.assertEqual(self.dummy.initiative(), self.dummy.initiative())


    def test_takeDamage(self):
        while not self.dummy.isDead():
            hp = self.dummy.hp
            self.dummy.takeDamage(1)
            self.assertGreater(hp, self.dummy.hp)
        self.mockTeam.moveToGrave.assert_called_once_with(self.dummy)

    def test_dealDamage(self):
        self.dummy.dealDamage(self.mockTarget, 1)
        self.mockTarget.takeDamage.assert_called_once_with(1)
        self.mockTarget.isDead = MagicMock(return_value=True)
        self.assertTrue(self.dummy.dealDamage(self.mockTarget, 1))

    def test_targetSelection(self):
        self.mockTeam.getEnemies = MagicMock(side_effect = IndexError)
        self.assertIsNone(self.dummy.selectTarget())
        self.mockTeam.getEnemies = MagicMock(return_value=[self.mockTarget])
        self.assertIs(self.dummy.selectTarget(), self.mockTarget)
        self.assertIs(self.dummy.target, self.mockTarget)

    def test_takeTurn(self):
        # TODO check stats increment
        self.mockTeam.getEnemies = MagicMock(return_value=[self.mockTarget])
        self.dummy.selectTarget()
        self.mockTarget.isDead = MagicMock(return_value=False)
        # make sure it doesn't hit
        self.mockTarget.ac = 100
        self.assertEqual(self.dummy.takeTurn(), [])
        self.mockTarget.takeDamage.assert_not_called()
        # make sure it does hit
        self.mockTarget.ac = 0
        
        self.assertEqual(self.dummy.takeTurn(), [])
        self.mockTarget.takeDamage.assert_called()
        self.mockTarget.isDead.assert_called()
        # make the target die
        self.mockTarget.isDead = MagicMock(return_value=True)
        self.assertEqual(self.dummy.takeTurn(), [self.mockTarget])
        self.assertIsNone(self.dummy.target)
        self.mockTeam.getEnemies = MagicMock(return_value=[])
        self.assertEqual(self.dummy.takeTurn(), [])


class InitiativeOrderTest(test.TestCase):
    
    def setUp(self):
        self.mockUnitList = [ MagicMock(spec=SimUnit) for i in range(8) ]
        for i in range(len(self.mockUnitList)):
            self.mockUnitList[i].initiative = MagicMock(return_value = i)
        
        self.initiative = InitiativeOrder()
    
    def test_initialization(self):
        self.assertTrue(hasattr(self.initiative, 'order'))
        self.assertTrue(hasattr(self.initiative, 'current'))
        self.initiative = InitiativeOrder(self.mockUnitList)
        self.assertNotEqual(self.initiative.order, [])
        
    def test_add_removeUnits(self):
        firstUnit = MagicMock(spec=SimUnit)
        firstUnit.initiative = MagicMock(return_value=100)
        lastUnit = MagicMock(spec=SimUnit)
        lastUnit.initiative = MagicMock(return_value=-100)
        self.initiative.add(firstUnit)
        self.assertListEqual(self.initiative.order, [firstUnit])
        self.initiative.add(lastUnit)
        self.assertListEqual(self.initiative.order, [firstUnit, lastUnit])
        self.initiative.add(*self.mockUnitList)
        self.assertEqual(len(self.initiative.order), len(self.mockUnitList) + 2)
        self.assertIs(self.initiative.order[0], firstUnit)
        self.assertIs(self.initiative.order[-1], lastUnit)

        self.assertEqual(self.initiative.remove(firstUnit, lastUnit), (firstUnit, lastUnit))
        self.assertNotIn(firstUnit, self.initiative.order)
        self.assertNotIn(lastUnit, self.initiative.order)
    
    def test_iteration(self):
        firstUnit = MagicMock(spec=SimUnit)
        firstUnit.initiative = MagicMock(return_value = 100)
        lastUnit = MagicMock(spec=SimUnit)
        lastUnit.initiative = MagicMock(return_value = -100)
        otherUnit = MagicMock(spec=SimUnit)
        otherUnit.initiative = MagicMock(return_value = 4)
        self.initiative.add(firstUnit)
        self.initiative.add(lastUnit)
        self.initiative.add(otherUnit)
        self.initiative.add(*self.mockUnitList)

        previous = firstUnit.initiative() + 1
        for unit in self.initiative:
            self.assertTrue(unit.initiative() <= previous)
            if unit is firstUnit:
                self.initiative.remove(lastUnit)
                self.assertNotIn(lastUnit, self.initiative.order)
            elif unit is otherUnit:
                self.initiative.remove(firstUnit)
                self.assertNotIn(firstUnit, self.initiative.order)
            self.assertIsNot(unit, lastUnit)
        
        for unit in self.initiative:
            self.assertIsNot(firstUnit, unit)

    def test_top(self):
        firstUnit = MagicMock(spec=SimUnit)
        firstUnit.initiative = MagicMock(return_value=1)
        lastUnit = MagicMock(spec=SimUnit)
        lastUnit.initiative = MagicMock(return_value=0)
        self.initiative.add(firstUnit, lastUnit)

        self.assertIs(firstUnit, next(self.initiative))
        self.assertIs(lastUnit, next(self.initiative))
        try:
            next(self.initiative)
            self.assertFalse(False)
        except StopIteration:
            self.assertTrue(True)


class SimArmyTest(test.TestCase):

    def setUp(self):
        self.dummyStats = base_statblock
        self.teamFoo = SimArmy([self.dummyStats for x in range(8)])
        self.unitFoo = choice(list(self.teamFoo.units))
        self.teamBar = SimArmy([self.dummyStats for x in range(8)])
        self.unitBar = choice(list(self.teamBar.units))
        self.teamBaz = SimArmy([self.dummyStats for x in range(8)])
        self.unitBaz = choice(list(self.teamBaz.units))

    def test_initialization(self):
        self.assertIn(self.unitFoo, self.teamFoo.units)
        self.assertFalse(self.teamFoo.grave)
        self.assertFalse(self.teamFoo.opponents)
    
    def test_addOpponent(self):
        self.teamFoo.addOpponents(self.teamBar)
        self.assertIn(self.unitBar, self.teamFoo.getEnemies())

    def test_addUnits(self):
        # TODO
        """
        invariant - all units in team are a subclass of SimUnit
        positive cases -
        * add SimUnit
        ** assert in team
        * add StatBlock
        ** assert something was added
        ** assert everything in units is SimUnit
        
        negative cases -
        * add object not issubclass(StatBlock)
        ** raise ValueError
        """
        mockUnit = MagicMock(spec=SimUnit)
        self.assertNotIn(mockUnit, self.teamFoo.units)
        self.teamFoo.addUnits(mockUnit)
        self.assertIn(mockUnit, self.teamFoo.units)
        beforeLength = len(self.teamFoo.units)
        self.teamFoo.addUnits(base_statblock)
        afterLegnth = len(self.teamFoo.units)
        self.assertGreater(afterLegnth, beforeLength)
        self.assertTrue(all([isinstance(unit, SimUnit) for unit in self.teamFoo.units]))
        # test adding many units
        beforeLength = len(self.teamFoo.units)
        adding = 3
        self.teamFoo.addUnits(*[base_statblock for x in range(adding)])
        afterLength = len(self.teamFoo.units)
        self.assertEqual(beforeLength + adding, afterLength)
        with self.assertRaises(ValueError):
            self.teamFoo.addUnits(object())

    def test_moveToGrave(self):
        for unit in list(self.teamFoo.units):
            unit.die()
        self.assertFalse(self.teamFoo.units)
        self.assertIn(self.unitFoo, self.teamFoo.grave)

    def test_isDone(self):
        self.teamFoo.addOpponents(self.teamBar, self.teamBaz)
        self.teamBar.addOpponents(self.teamFoo, self.teamBaz)
        self.teamBaz.addOpponents(self.teamBar)
        self.assertFalse(self.teamFoo.isDone())
        self.assertFalse(self.teamBar.isDone())
        self.assertFalse(self.teamBaz.isDone())
        for unit in list(self.teamBar.units):
            unit.die()
        self.assertTrue(self.teamBar.isDone())
        self.assertTrue(self.teamBaz.isDone())
        self.assertTrue(self.teamBaz.survived())
        self.assertFalse(self.teamFoo.isDone())
        for unit in list(self.teamBaz.units):
            unit.die()
        self.assertTrue(self.teamFoo.isDone())
        self.assertTrue(self.teamFoo.survived())
        self.assertFalse(self.teamBaz.survived())
    
class TwoSidedEncounterTest(test.TestCase):

    def setUp(self):
        self.dummyStats = base_statblock
        self.teamFoo = SimArmy([self.dummyStats for x in range(10)])
        self.teamBar = SimArmy([self.dummyStats for x in range(10)])
        self.teamFoo.addOpponents(self.teamBar)
        self.teamBar.addOpponents(self.teamFoo)
        self.sim = EncounterSim(self.teamFoo, self.teamBar)
    
    def test_initialization(self):
        """
        * winner is none
        * initiative is type initiative
        * each army is in the sides
        """
        self.assertIsNone(self.sim.winner)
        self.assertFalse(self.sim.started)
        self.assertIn(self.teamFoo, self.sim.sides)
        self.assertIn(self.teamBar, self.sim.sides)
        self.assertIsInstance(self.sim.initiative, InitiativeOrder)

    def test_rollInitiative(self):
        fooGuy = choice(list(self.teamBar.getUnits()))
        self.assertFalse(self.sim.initiative.order)
        self.assertFalse(self.sim.started)
        self.sim.rollInitiative()
        self.assertTrue(self.sim.initiative.order)
        self.assertIn(fooGuy, self.sim.initiative)
        self.assertTrue(fooGuy.initiative())
        self.assertTrue(self.sim.started)

    def test_isDone(self):
        self.assertFalse(self.teamFoo.isDone())
        self.assertFalse(self.teamBar.isDone())
        self.assertFalse(self.sim.isDone())
        for unit in list(self.teamBar.getUnits()):
            unit.die()
        self.assertTrue(self.sim.isDone())
        self.assertIs(self.teamFoo, self.sim.declareWinner())

    def test_runRound(self):
        self.assertRaises(Exception, self.sim.runRound)
        self.sim.rollInitiative()
        self.assertFalse(self.sim.runRound())
        for unit in list(self.teamBar.getUnits()):
            unit.die()
        self.assertTrue(self.sim.runRound())

    def test_addUnits(self):
        # TODO
        """
        positive case:
        * add SimUnit/StatBlock to teams in the encounter
        ** before - unit not in team, initiative
        ** assert unit in team
        ** assert unit in initiative
        negative case:
        * add SimUnit to team not in the encounter
        ** assert raises ValueError
        """
        baz = SimUnit(base_statblock, self.teamFoo)
        self.assertNotIn(baz, self.teamFoo.units)
        self.assertNotIn(baz, self.sim.initiative)
        self.sim.addUnits(self.teamFoo, baz)
        self.assertIn(baz, self.teamFoo.units)
        self.assertIn(baz,self.sim.initiative)
        mockTeam = MagicMock(spec=SimArmy)
        with self.assertRaises(ValueError):
            self.sim.addUnits(mockTeam, baz)

    def test_run(self):
        self.assertFalse(self.sim.isDone())
        self.sim.run()
        self.assertTrue(self.sim.isDone())