# DnD Fight Module

## Overview
Side project that evolved from wanting to calculate the relative strength of various critical damage systems.
Started by representing dice as a tuple of (num_dice, dice_value), then extended it to include smites and a rudimentary fight simulator

Want to continue to extend this to the point where characters and creatures can be easily loaded up and used in combat simulations

## TODO
  - finish enounter simulation
  - implement character data parsing using pyparsing!
  - implement monte carlo simulation
  - implement simulation configuration files
  - go through and pretty things up with typing

## High Level Capabilities
  - Dice Roll Simulation __(core)__
  - Simulate a combat encouter
  - Nice Abstraction of Characters, Weapons, Etc. __(nice to have)__
  - Graphing / Nice output __(nice to have)__
    - pyplot etc
  - Optional Fight Output __(nice to have)__
  - Full Fight Simulation __(nice to have)__
    - multiple actions (block etc)

## Core Mechanics
  - Attack and Damage Rolls
  - Saving Throws
  - Advantage/Disadvantage
  - Critical Hits
  - Spells (nice to have)

## Module Contents

  ### Core
  Contains modules to facilitate core rules, mechanics, and functionality
    - Dice rolling simulation
    - Ability Scores and Skills
    - Actions
    - Defining turns
  
  ### Items
  Contains modules to create/represent items
    - Items, Weapons, Armor, Potions etc
    - Inventory management

  ### Characters
  Contains modules for create/represent characters
    - Basic Stat blocks
    - Player Characters, creating them, reading in from files
    - Monsters enemies as well

  ### Simulation
  Defines monte carlo and other simulations to run
    - trial definitions
    - running a simulation
    - output and modeling

  ### Data
    - Predefined characters
    - simulation output
    - tables for character creation


## Current Ideas

  ### Seperate Simulation Module
    - pull out the code that simulates fights, and runs multiple trials in a way that makes consuming I/O easier

  ### Character Class
  - includes ability scores, stats, levels, inventory, description etc
  - extends from the basic StatBlock
  - read in an annotated text file load class

  ### Simulation Output
  - get more information out of simulations by consuming their output and transforming into more useful representations
  - graphs, logs, more stats

  ### Detailed Simulation
  - take user input to influence simulation
  - more actions than just attack, blocking to impose disadvantage, allow for abilities that impose adv/dis
  - implement rudimentary ai 