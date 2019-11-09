"""
reads in a character sheet file and returns a python dictionary of the necessary data
"""

import sys
from collections import deque, namedtuple
import argparse
import glob

from CharacterSheet import readCharacterSheet

parser = argparse.ArgumentParser(description="read in data from a character sheet file")
parser.add_argument("-d","--dir", 
                    help="directory to search for character files",
                    default="")
parser.add_argument("files", nargs=argparse.REMAINDER)

def main():
  args = parser.parse_args()
  charData = {}
  files = [ f"{args.dir}{file}" for file in args.files ]
  for filename in files:
    print(filename)
    charData[filename] = readCharacterSheet(filename)
    for field in charData[filename]:
      print(f"{field} : {charData[filename][field]}")
    print()



if __name__ == '__main__':
  main()