import os
import json
from pyvis.network import Network
from utils.loaders import load_relationships, load_subject_nodes


# =========================================================
# Helper Function — Create Clickable Label
# =========================================================
def clickable_label(text, subject=None):
    """
    Produce HTML label for a PyVis node.
    If subject is provided → clickable link opens Subject Browser.
    """
    if subject:
        link = f"/Subject_Browser?subject={subject}&node={text}"
        return f'<a href="{link}" target="_parent">{text}</a>'
    else:
        return f'<span style="color:#bbb;">{text}</span>'  # non-clickable (missing node)


# =========================================================
# Build SUBJECT Graph (auto-add missing nodes)
# =========================================================
def build_subject_graph(subject):

    nodes = load_subject_nodes(subject)
    relationships = load_relationships(subject)

    output_path = f"{subject}_graph.html"

    # Create PyVis graph
    net = Network(
        height="750px",
        width="100%",
        directed=True,
        bgcolor="#202020",
        font_color="white"
    )

    # More stable layout
    net.force_atlas_2based(gravity=-50)

    # ---------------------------------------------------------
    # 1. Add existing nodes (clickable)
    # ---------------------------------------------------------
    for node_name in nodes.keys():
        net.add_node(
            node_name,
            label=clickable_label(node_name, subject),
            title=node_name,
            shape="dot",
            size=18,
            color="#6AAFFF",     # blue for real nodes
        )

    # ---------------------------------------------------------
    # 2. Add missing nodes (non-clickable gray)
    # ---------------------------------------------------------
    for edge in relationships:
        src = edge["source"]
        tgt = edge["target"]

        # Add source if missing
        if src not in net.get_nodes():
            net.add_node(
                src,
                label=clickable_label(src, None),
                title=f"{src} (missing node file)",
                shape="dot",
                size=14,
                color="#888888",
            )

        # Add target if missing
        if tgt not in net.get_nodes():
            net.add_node(
                tgt,
                label=clickable_label(tgt, None),
                title=f"{tgt} (missing node file)",
                shape="dot",
                size=14,
                color="#888888",
            )

    # ---------------------------------------------------------
    # 3. Add edges
    # ---------------------------------------------------------
    for edge in relationships:
        src = edge["source"]
        tgt = edge["target"]
        rel = edge.get("relation", "")

        net.add_edge(src, tgt, title=rel)

    # Save interactive HTML
    net.save_graph(output_path)
    return output_path


# =========================================================
# Build GLOBAL Graph (merged subjects)
# =========================================================
def build_global_graph():

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    merged_path = os.path.join(base_dir, "global_kg", "merged_graph.json")

    if not os.path.exists(merged_path):
        raise FileNotFoundError(f"Global KG not found: {merged_path}")

    with open(merged_path, "r") as f:
        edges = json.load(f)

    output_path = "global_graph.html"

    # Graph object
    net = Network(
        height="850px",
        width="100%",
        directed=True,
        bgcolor="#202020",
        font_color="white"
    )

    net.force_atlas_2based(gravity=-50)

    # ---------------------------------------------------------
    # 1. Build mapping from node → subject
    # ---------------------------------------------------------
    subjects_dir = os.path.join(base_dir, "subjects")
    subject_map = {}

    for subject in os.listdir(subjects_dir):
        subnodes = load_subject_nodes(subject)
        for node in subnodes.keys():
            subject_map[node] = subject

    # ---------------------------------------------------------
    # 2. Add nodes (clickable if we know the subject)
    # ---------------------------------------------------------
    for edge in edges:
        src = edge["source"]
        tgt = edge["target"]

        # SOURCE node
        if src not in net.get_nodes():
            if src in subject_map:
                label = clickable_label(src, subject_map[src])
                color = "#6AAFFF"
            else:
                label = clickable_label(src, None)
                color = "#999999"

            net.add_node(src, label=label, color=color)

        # TARGET node
        if tgt not in net.get_nodes():
            if tgt in subject_map:
                label = clickable_label(tgt, subject_map[tgt])
                color = "#6AAFFF"
            else:
                label = clickable_label(tgt, None)
                color = "#999999"

            net.add_node(tgt, label=label, color=color)

        # Add edge
        net.add_edge(src, tgt)

    # Save file
    net.save_graph(output_path)
    return output_path
