# Import functions from other scripts
import sys
import networkx as nx
import statistics as stat

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


    print(f"Exporting generated AGG dictionary. \n Number of scenes: {len(agg_dict["scenes"])} \n Number of musical pieces: {len(agg_dict["music"])}")
    dict2json(agg_dict,output_filename)

    return agg_dict


def generate_networkx_graph(agg_dict,output_filename,base_url="https://nicholascorniaorpheus.github.io/a_gothic_gamebook/",value= 100,color="#a55faa"):
    # initialize network
    net = nx.DiGraph()
    # add nodes based on scenes
    for scene in agg_dict["scenes"]:
        image = f"""<img src="{base_url}scene/{scene["label"][0]}.webp" width="250" height="200">"""
        # merging potential multiple musical pieces in unique string
        # get music information
        music_list = list(filter(lambda x: x["label"][0] in scene["music"], agg_dict["music"]))
        music_string = str(", ".join([music for music in scene["music"]]))
        if len(scene["goes_to"]) <= 1:
            if len(scene["change_spotlight"]) == 0:
                public_choice = False
            else:
                public_choice = True 
        else:
            public_choice = True 

        title = (
                """
            <body>
            <h3> <a href='""" 
                + base_url + """scene/""" + scene["label"][0]
                + """'>"""
                + scene["label"][0]
                + """</a></h3>
            <p>"""
                + scene["argument"][0]
                + "Musical pieces: " + music_string +"""</p>"""
                + image +
                """
            </body>
            """
            )
        net.add_node(scene["id"],
                    label = scene["label"][0],
                    color= color,
                    value= value,
                    title = title,
                    music = music_list,
                    public_choice = public_choice
                    )

    # add edges
    for scene in agg_dict["scenes"]:
        try:
            for node in scene["goes_to"]:
                # retrieve node id based on label
                if node != "":
                    query_node = list(filter(lambda x: x["label"][0] == node, agg_dict["scenes"]))
                    try:
                        query_node = query_node[0]
                    except IndexError:
                        print(scene["id"])
                        print(query_node)
                    # add edge using net.add_edge
                    net.add_edge(scene["id"],query_node["id"],weight=10)
        except KeyError:
            pass 
        # add special paths by changing spotlight
        try:
            for node in scene["change_spotlight"]:
                if node != "":
                    # retrieve node id based on label
                    try:
                        query_node = list(filter(lambda x: x["label"][0] == node, agg_dict["scenes"]))[0]
                    except IndexError:
                        print(scene["id"])
                        print(query_node)
                    # add edge using net.add_edge
                    net.add_edge(scene["id"],query_node["id"],weight=1)
        except KeyError:
            pass

    # check consistency by double-checking "comes_from" property.

    # TO DO

    print(f'Exporting Networkx graph in JSON format')
    net_dict = nx.node_link_data(net, edges="links")
    dict2json(net_dict,output_filename)

    return net


# Return plots, first order statistics and some graph properties concerning connectivity, path length etc...
def generate_graph_statistics(agg_graph,agg_dict,output_filename,scene_argument_timing=1,public_choice_timing=2):

    statistics = {}

    # get sources and sinks
    sources = list(filter(lambda x: agg_graph.in_degree(x) == 0, agg_graph.nodes()))
    sinks = list(filter(lambda x: agg_graph.out_degree(x) == 0, agg_graph.nodes()))
    statistics["sources"] = {}
    statistics["sinks"] = {}
    statistics["sources"]["nodes"] = sources
    statistics["sinks"]["nodes"] = sinks
    statistics["sources"]["value"] = len(sources)
    statistics["sinks"]["value"] = len(sinks)

    # get all possible paths from sources to sinks

    all_paths = []

    for source in sources:
        for sink in sinks:
            all_paths.append(list(nx.all_simple_paths(agg_graph,source,sink)))
    sum_length = 0
    number_trajectories = 0
    timing_paths = 0
    occurrence_scene = []
    for node in agg_graph.nodes():
        try:
            occurrence_scene.append({"id": node, "label": agg_graph.nodes[node]["label"], "occurrence": 0.0})
        except KeyError:
            print(agg_graph.nodes[node])

    for source_trajectories in all_paths:
        for path in source_trajectories:
            sum_length += len(path)
            number_trajectories +=1
            timing_paths += len(path)*scene_argument_timing
            # count public_choices moments
            for node in path:
                # calculate occurrence
                occurrence_scene[node]["occurrence"] += 1
                # add timing for chocies and songs
                if agg_graph.nodes[node]["public_choice"]:
                    timing_paths += public_choice_timing
                for song in agg_graph.nodes[node]["music"]:
                    timing_paths += float(song["duration"][0])


    statistics["paths"] = {}
    statistics["paths"]["average_length"]  = float(sum_length)/number_trajectories
    statistics["paths"]["average_duration_performance"] = float(timing_paths)/number_trajectories
    statistics["paths"]["number_of_trajectories"] = number_trajectories
    statistics["paths"]["trajectories"] = all_paths

    for node in occurrence_scene:
        node["occurrence"] = node["occurrence"]/number_trajectories

    statistics["paths"]["scene_occurrence"] = {}
    occurrence_list = list(node["occurrence"] for node in occurrence_scene)
    statistics["paths"]["scene_occurrence"]["standard_deviation"] = stat.stdev(occurrence_list)
    statistics["paths"]["scene_occurrence"]["average"] = sum([node["occurrence"] for node in occurrence_scene])/len(occurrence_scene)
    statistics["paths"]["scene_occurrence"]["nodes"] = occurrence_scene
    

    print(f"Exporting statistics...")

    dict2json(statistics,output_filename)
         


    return statistics
