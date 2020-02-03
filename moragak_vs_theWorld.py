"""
proof of concept, moragak vs 100 peasants
"""

from itertools import count

from DndDice import D12, D8, D6
from StatBlock import base_statblock, MoragakStats
from Encounter import EncounterSim, SimArmy
from AttackAction import AttackAction

bigAxe = AttackAction('big axe', D12, (7, 4), 'slashing')
MoragakStats.addAttackAction(bigAxe)

def main():
    teamMoragak = SimArmy([MoragakStats])
    peasantPool = [base_statblock for x in range(100)]
    teamPeasants = SimArmy([peasantPool.pop() for i in range(8)])
    teamMoragak.addOpponents(teamPeasants)
    teamPeasants.addOpponents(teamMoragak)
    sim = EncounterSim(teamMoragak, teamPeasants)
    sim.rollInitiative()
    countRound = count(1,1)
    while not sim.isDone():
        sim.runRound()
        rem = len(sim.initiative)
        if rem < 8:
            while len(peasantPool) and len(sim.initiative) < 8:
                sim.addUnits(teamPeasants, peasantPool.pop())
    sim.declareWinner()

    if sim.winner == teamMoragak:
        print("Moragak Wins!")
    else:
        print("the peasants prevail")
        print(f"{len(peasantPool) + len(teamPeasants.units)} remain")


def exampleSim():
    """
    # start off by creating  StatBlocks
    # StatBlock(str->name,
    #           int->hp,
    #           int->ac,
    #           list->ability scores)
    """
    HimoStats = StatBlock('Himo', 37, 17, [15, 16, 11, 14, 14, 18])
    LaviStats = StatBlock('Lavi', 42, 18, [9, 18, 13, 18, 14, 13])

    # add attack action
    # AttackAction(str->name,
    #              Dice->dmg dice
    #              tuple->(atkMod,dmgMod),
    #              str->damagetype)
    rapier = AttackAction('rapier', D8, (6, 3), 'piercing')
    HimoStats.addAttackAction(rapier)
    crossbow = AttackAction('crossbow', D6, (7, 4), 'piercing')
    LaviStats.addAttackAction(crossbow)
    
    # create sim army out of statblocks
    teamHimo = SimArmy(Himo)
    teamLavi = SimArmy(Lavi)

    # set up opposing sides before starting the encounter
    teamHimo.addOpponents(teamLavi)
    teamLave.addOpponents(teamHimo)

    # set up the simulation
    sim = EncounterSim(teamHimo, teamLavi)
    # run it
    sim.run()
    # inspect the winner in sim.winner
    

if __name__ == "__main__":
    main()
    