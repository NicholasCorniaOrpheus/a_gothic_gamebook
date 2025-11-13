"""
Python script to generate statistics and graph analysis of the storypath of A Gothic Gamebook
"""
import sys

sys.path.append("./modules")  # importing custom functions in modules
from modules.utilities import *
from modules.analysis import *

"""TO DO
- [x ] import scenes and music from csv files from Obsidian/Google Drive
- [x ] get start_scenes => comes_from = {}
- [x ] get end_scenes => goes_to = {}
- [ ] for each scene public_choice => goes_to > 1
- [x ] change_spotlight is counting for the in and outdegree, but the outcomes are randomly selected by the GM.
- [x ] use networkx for analysis
- [x] generate recursively all possible paths as list, taking into account change_spotlight
- [x ] calculate statistics for path length, number of public_choices, music pieces length.


"""

#### CODE ####

scenes_csv_filename = os.path.join("data", "agg_scenes.csv")

music_csv_filename = os.path.join("data", "agg_music.csv")

mapping_filename = os.path.join("mappings", "csv2dict_mapping.csv")

agg_dictionary_filename = os.path.join("data", "agg_dict.json")

agg_networkx_graph_filename = os.path.join("data", "agg_networkx.json")

agg_statistics_filename = os.path.join("data", "agg_statistics.json")

agg_dict = csvs_to_scenes_dictionary(
    scenes_csv_filename,
    music_csv_filename,
    mapping_filename,
    agg_dictionary_filename,
    separator=",",
)

agg_graph = generate_networkx_graph(agg_dict, agg_networkx_graph_filename)

generate_graph_statistics(agg_graph, agg_dict, agg_statistics_filename)
