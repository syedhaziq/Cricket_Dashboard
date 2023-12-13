import sys
import logging
import os
# from os.path import abspath, join, dirname

# logging.info(f"This is a log message with variable: {os.getcwd()}")
from player_info import player_info
from batter  import batter_stats
from all_rounder_stats import allrounder_stats
from bowlers_stats import bowlers_stats


def main():
    player_info()
    batter_stats()
    allrounder_stats()
    bowlers_stats()



if __name__ == "__main__":
    main()