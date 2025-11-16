import os
import json
from pyvis.network import Network
from utils.loaders import load_subject_nodes, load_relationships


# ============================================================
# Utility: Inject JavaScript so node clicks update URL
# ============================================================
def inject_js_into_html(html_path):
    """Injects JavaScript into PyVis HTML to send node click events to Streamlit."""

    js_code = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        if (typeof network !== 'undefined') {
            network.on("click", function(params) {

                if (params.nodes && params.nodes.length > 0) {
                    const nodeId = params.nodes[0];

                    const parent = window.parent;
                    const base = parent.location.origin + parent.location.pathname;
                    const newUrl = base + "?selected_node=" + encodeURIComponent(nodeId);

                    parent.history.replaceState(null, "", newUrl);
                }
            });
        }
    });
    </script>
    """

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    if "</body>" in html_content:
        html_content = html_content.replace("</body>", js_code + "</body>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)


# ============================================================
# SUBJECT GRAPH BUILDER
# ============================================================
def build_subject_graph(subject):
    """
    Build PyVis graph for a specific subject.
    Returns the path to the generated HTML.
    """

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    nodes_dir = os.path.join(base_dir, "subjects", subject, "nodes")
    rels_dir = os.path.join(base_dir, "subjects", subject, "relationships")

    # Load nodes + edges
    nodes = load_subject_nodes(subject)
    relationships = load_relationships(subject)

    output_path = f"{subject}_graph.html"

    # Configure PyVis
    net = Network(
        height="750px",
        width="100%",
        directed=True,
        bgcolor="#202020",
        font_color="white",
    )
    net.force_atlas_2based()

    # Add existing nodes (blue)
    for node_name in nodes.keys():
        net.add_node(
            node_name,
            label=node_name,
            title=node_name,
            shape="dot",
            size=18,
            color="#6AAFFF",  # blue
        )

    # Add missing nodes (gray)
    for edge in relationships:
        src = edge["source"]
        tgt = edge["target"]

        if src not in net.get_nodes():
            net.add_node(src, label=src, color="#999999", size=14)

        if tgt not in net.get_nodes():
            net.add_node(tgt, label=tgt, color="#999999", size=14)

    # Add edges
    for edge in relationships:
        net.add_edge(edge["source"], edge["target"], title=edge.get("relation", ""))

    # Save HTML
    net.save_graph(output_path)

    # Add JS for node click → sidebar selection
    inject_js_into_html(output_path)

    return output_path


# ============================================================
# GLOBAL GRAPH BUILDER
# ============================================================
def build_global_graph():
    """
    Build PyVis graph combining all subjects.
    Returns path to generated HTML.
    """

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    merged_path = os.path.join(base_dir, "global_kg", "merged_graph.json")

    if not os.path.exists(merged_path):
        raise FileNotFoundError(f"Global KG not found: {merged_path}")

    with open(merged_path, "r") as f:
        relationships = json.load(f)

    output_path = "global_graph.html"

    net = Network(
        height="800px",
        width="100%",
        directed=True,
        bgcolor="#202020",
        font_color="white",
    )
    net.force_atlas_2based()

    # Map nodes → subjects
    subjects_dir = os.path.join(base_dir, "subjects")
    subject_map = {}

    for subject in os.listdir(subjects_dir):
        nodes = load_subject_nodes(subject)
        for node in nodes.keys():
            subject_map[node] = subject

    # Add all nodes + edges
    for edge in relationships:
        src = edge["source"]
        tgt = edge["target"]

        for n in [src, tgt]:
            if n not in net.get_nodes():
                color = "#6AAFFF" if n in subject_map else "#999999"
                net.add_node(
                    n,
                    label=n,
                    size=16,
                    color=color,
                )

        net.add_edge(src, tgt, title=edge.get("relation", ""))

    # Save HTML
    net.save_graph(output_path)

    # Inject click-handler JS
    inject_js_into_html(output_path)

    return output_path
