"""
Python script to generate statistics and graph analysis of the storypath of A Gothic Gamebook
"""
import sys

sys.path.append("./modules")  # importing custom functions in modules
from modules.utilities import *
from modules.analysis import *
from modules.markdown import *

#### CODE ####

scenes_csv_filename = os.path.join("data", "agg_scenes.csv")

music_csv_filename = os.path.join("data", "agg_music.csv")

mapping_filename = os.path.join("mappings", "csv2dict_mapping.csv")

agg_dictionary_filename = os.path.join("data", "agg_dict.json")

agg_networkx_graph_filename = os.path.join("data", "agg_networkx.json")

agg_storypath_graph_filename = os.path.join(
    "overrides", "assets", "storypath", "agg_2025_storypath.html"
)

agg_statistics_filename = os.path.join("data", "agg_statistics.json")

agg_music_markdown_directory = os.path.join("docs", "music")

agg_scenes_markdown_directory = os.path.join("docs", "scenes")

base_url = "https://nicholascorniaorpheus.github.io/a_gothic_gamebook"


print("Generate dictionary from CSV input...")

agg_dict = csvs_to_scenes_dictionary(
    scenes_csv_filename,
    music_csv_filename,
    mapping_filename,
    agg_dictionary_filename,
    separator=",",
)

print("Generate Markdown pages for scenes and songs...")

generate_scenes_md(agg_dict, agg_scenes_markdown_directory, base_url)

print("Generate storypath graph and statistics...")

agg_graph = generate_networkx_graph(agg_dict, agg_networkx_graph_filename)

pyvis_visualization(agg_graph, agg_storypath_graph_filename)

generate_graph_statistics(agg_graph, agg_dict, agg_statistics_filename)
