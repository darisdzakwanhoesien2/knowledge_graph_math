import os
from pyvis.network import Network
from utils.loaders import load_relationships

def build_subject_graph(subject):
    edges = load_relationships(subject)
    output_path = f"{subject}_graph.html"

    net = Network(height="800px", width="100%", directed=True)
    net.force_atlas_2based()

    for edge in edges:
        s, t, r = edge["source"], edge["target"], edge["relation"]
        net.add_node(s, label=s)
        net.add_node(t, label=t)
        net.add_edge(s, t, title=r)

    net.save_graph(output_path)
    return output_path


def build_global_graph():
    path = "../../global_kg/merged_graph.json"
    output_path = "global_graph.html"

    with open(path, "r") as f:
        data = f.load()

    net = Network(height="800px", width="100%", directed=True)
    net.force_atlas_2based()

    for edge in data:
        s, t = edge["source"], edge["target"]
        net.add_node(s, label=s)
        net.add_node(t, label=t)
        net.add_edge(s, t)

    net.save_graph(output_path)
    return output_path
