"""
Python script to generate statistics and graph analysis of the storypath of A Gothic Gamebook
"""
import sys

sys.path.append("./modules")  # importing custom functions in modules
from modules.utilities import *
from modules.analysis import *

"""TO DO
- [ ] import scenes and music from csv files from Obsidian/Google Drive
- [ ] get start_scenes => comes_from = {}
- [ ] get end_scenes => goes_to = {}
- [ ] for each scene public_choice => goes_to > 1
- [ ] for each scene, determine "level" according to tree structure (no loops)
- [ ] change_spotlight_currency => switch character, randomly decide next scene from other character starting from current"level"
- [ ] track both X and Y position of characters in story.
- [ ] generate recursively all possible paths as list, including change_spotlight options.
- [ ] calculate statistics for path length, number of public_choices, music pieces length.
- [ ] generate graph using networkx and pyvis? Or try other Javascript module via Pandas?

"""

#### CODE ####

scenes_csv_filename = os.path.join("data", "agg_scenes.csv")

music_csv_filename = os.path.join("data", "agg_music.csv")

mapping_filename = os.path.join("mappings", "csv2dict_mapping.csv")

agg_dictionary_filename = os.path.join("data", "agg_dict.json")

csvs_to_scenes_dictionary(
    scenes_csv_filename,
    music_csv_filename,
    mapping_filename,
    agg_dictionary_filename,
    separator=",",
)
