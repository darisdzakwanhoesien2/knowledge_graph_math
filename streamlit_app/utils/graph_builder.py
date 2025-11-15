import os
import json
from pyvis.network import Network
from utils.loaders import load_relationships, load_subject_nodes


# =========================================================
# Build SUBJECT Graph (with auto-add missing nodes)
# =========================================================
def build_subject_graph(subject):
    nodes = load_subject_nodes(subject)
    relationships = load_relationships(subject)

    output_path = f"{subject}_graph.html"

    net = Network(
        height="750px",
        width="100%",
        directed=True,
        bgcolor="#202020",
        font_color="white",
    )

    net.force_atlas_2based()

    # ---------------------------------------------------------
    # 1. Add EXISTING nodes (with clickable links)
    # ---------------------------------------------------------
    for node_name in nodes.keys():
        href = f"/Subject_Browser?subject={subject}&node={node_name}"
        net.add_node(
            node_name,
            label=node_name,
            title=node_name,
            shape="dot",
            size=18,
            color="#6AAFFF",
            href=href,
        )

    # ---------------------------------------------------------
    # 2. Add MISSING nodes found only in relationships
    # ---------------------------------------------------------
    for edge in relationships:
        src = edge["source"]
        tgt = edge["target"]

        # Source node missing
        if src not in net.get_nodes():
            net.add_node(
                src,
                label=src,
                title=f"{src} (missing node file)",
                color="#999999",  # GRAY for missing
                shape="dot",
                size=16,
            )

        # Target node missing
        if tgt not in net.get_nodes():
            net.add_node(
                tgt,
                label=tgt,
                title=f"{tgt} (missing node file)",
                color="#999999",
                shape="dot",
                size=16,
            )

    # ---------------------------------------------------------
    # 3. Add edges AFTER all nodes exist
    # ---------------------------------------------------------
    for edge in relationships:
        src = edge["source"]
        tgt = edge["target"]
        rel = edge.get("relation", "")
        net.add_edge(src, tgt, title=rel)

    net.save_graph(output_path)
    return output_path


# =========================================================
# Build GLOBAL Graph (also auto-add missing nodes)
# =========================================================
def build_global_graph():
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
    merged_path = os.path.join(base_dir, "global_kg", "merged_graph.json")

    if not os.path.exists(merged_path):
        raise FileNotFoundError(f"Global KG not found: {merged_path}")

    with open(merged_path, "r") as f:
        edges = json.load(f)

    output_path = "global_graph.html"

    net = Network(
        height="800px",
        width="100%",
        directed=True,
        bgcolor="#202020",
        font_color="white",
    )
    net.force_atlas_2based()

    # Map nodes to subjects if possible
    subjects_dir = os.path.join(base_dir, "subjects")
    subject_map = {}

    for subject in os.listdir(subjects_dir):
        subnodes = load_subject_nodes(subject)
        for n in subnodes.keys():
            subject_map[n] = subject

    # Add nodes
    for edge in edges:
        src = edge["source"]
        tgt = edge["target"]

        # Source node
        if src not in net.get_nodes():
            if src in subject_map:
                href = f"/Subject_Browser?subject={subject_map[src]}&node={src}"
                color = "#6AAFFF"
            else:
                href = ""
                color = "#999999"

            net.add_node(src, label=src, href=href, color=color)

        # Target node
        if tgt not in net.get_nodes():
            if tgt in subject_map:
                href = f"/Subject_Browser?subject={subject_map[tgt]}&node={tgt}"
                color = "#6AAFFF"
            else:
                href = ""
                color = "#999999"

            net.add_node(tgt, label=tgt, href=href, color=color)

        # Add edge
        net.add_edge(src, tgt)

    net.save_graph(output_path)
    return output_path
