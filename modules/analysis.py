# Import functions from other scripts
import sys

sys.path.append("./modules")
from utilities import *


# Imports csv files from Obsidian/Google Drive and parse them in a JSON dictionary for analysis
def csvs_to_scenes_dictionary(
    scenes_csv_filename, music_csv_filename, mapping_filename, output_filename,separator=","
):
    # convert csvs to raw dictionary
    music_dict = csv2dict(music_csv_filename)
    scenes_dict = csv2dict(scenes_csv_filename)

    # import mapping
    mapping = csv2dict(mapping_filename)

    # initiate final dictionary

    agg_dict = {"scenes": [], "music": []}
    i = 0
    for scene in scenes_dict:
        agg_dict["scenes"].append({"id": i })
        i += 1
        for key in scene.keys():
            # map csv key with mapping key
            query = list(filter(lambda x: x["csv_field"] == key, mapping))
            if len(query) > 0:
                prop = query[0]["property"]
                # split according to separator
                if query[0]["separator"] == "true":
                    splitted_values = scene[key].split(",")
                    # append value to the dictionary.
                    for value in splitted_values:
                        try:
                            # exclude first empty space and deleting Obsidian Wiki brackets
                            agg_dict["scenes"][-1][prop].append(value[1:].replace("[[","").replace("]]",""))
                        except KeyError:
                            agg_dict["scenes"][-1][prop] = [value.replace("[[","").replace("]]","")]
                else: # singular case
                    agg_dict["scenes"][-1][prop] = [scene[key].replace("[[","").replace("]]","")]

    for music in music_dict:
        print(music)
        input()
        agg_dict["music"].append({"id": i })
        i += 1
        for key in music.keys():
            # map csv key with mapping key
            query = list(filter(lambda x: x["csv_field"] == key, mapping))
            if len(query) > 0:
                prop = query[0]["property"]
                # split according to separator
                if query[0]["separator"] == "true":
                    splitted_values = music[key].split(",")
                    # append value to the dictionary.
                    for value in splitted_values:
                        try:
                            agg_dict["music"][-1][prop].append(value[1:].replace("[[","").replace("]]",""))
                        except KeyError:
                            agg_dict["music"][-1][prop] = [value.replace("[[","").replace("]]","")]


                else: # singular case
                    agg_dict["music"][-1][prop] = [music[key].replace("[[","").replace("]]","")]


    print(f"Exporting generated AGG dictionary. Number of scenes: {len(agg_dict["scenes"])} \n Number of musical pieces: {len(agg_dict["music"])}")
    dict2json(agg_dict,output_filename)



    # TO BE CONTINUED


# Calculate properties, like in and outdegree, source, sink (directed graph terminology)...
def generate_derivative_properties(agg_dict):
    pass


# Recursively calculate all possible paths and record them in a list
def generate_possible_paths(agg_dict):
    pass


# Return plots, first order statistics and some graph properties concerning connectivity, path length etc...
def generate_graph_statistics(paths_list, agg_dict):
    pass
