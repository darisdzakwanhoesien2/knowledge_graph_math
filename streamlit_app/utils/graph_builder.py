import os
import json
from pyvis.network import Network

# Use a relative import so this module works regardless of how
# Streamlit resolves sys.path (avoids the brittle sys.path.append
# in the top-level streamlit_app.py).
from utils.loaders import load_subject_nodes, load_relationships


# ============================================================
# Utility: Inject JavaScript so node clicks update the URL
# ============================================================
def inject_js_into_html(html_path: str) -> None:
    """
    Append a <script> block to the PyVis HTML file so that
    clicking a graph node updates the parent window's URL with
    ?selected_node=<nodeId>.  Streamlit can then read that param
    and update the sidebar selection.
    """
    js_code = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        // `network` is the global PyVis/vis.js Network instance
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

    # Only inject once; guard against repeated calls on the same file
    if "</body>" in html_content and js_code.strip() not in html_content:
        html_content = html_content.replace("</body>", js_code + "</body>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)


# ============================================================
# Shared PyVis network factory
# ============================================================
def _make_network(height: str = "750px") -> Network:
    """Return a pre-configured directed PyVis Network."""
    net = Network(
        height=height,
        width="100%",
        directed=True,
        bgcolor="#202020",
        font_color="white",
    )
    net.force_atlas_2based()
    return net


# ============================================================
# SUBJECT GRAPH BUILDER
# ============================================================
def build_subject_graph(subject: str) -> str:
    """
    Build a PyVis graph for a single subject and write it to
    ``<subject>_graph.html`` in the current working directory.

    Blue nodes  (#6AAFFF) → have a corresponding Markdown file.
    Grey nodes  (#999999) → appear only in edges (no .md file yet).

    Returns the path to the generated HTML file.
    """
    nodes = load_subject_nodes(subject)
    relationships = load_relationships(subject)

    output_path = f"{subject}_graph.html"
    net = _make_network(height="750px")

    # Add nodes that have markdown files (blue)
    for node_name in nodes:
        net.add_node(
            node_name,
            label=node_name,
            title=node_name,
            shape="dot",
            size=18,
            color="#6AAFFF",
        )

    # Add nodes that only exist in edge definitions (grey)
    for edge in relationships:
        for key in ("source", "target"):
            node = edge[key]
            if node not in net.get_nodes():
                net.add_node(node, label=node, color="#999999", size=14)

    # Add directed edges
    for edge in relationships:
        net.add_edge(
            edge["source"],
            edge["target"],
            title=edge.get("relation", ""),
        )

    net.save_graph(output_path)
    inject_js_into_html(output_path)
    return output_path


# ============================================================
# GLOBAL GRAPH BUILDER
# ============================================================
def build_global_graph() -> str:
    """
    Build a PyVis graph that merges all subjects from the global
    KG file (``global_kg/merged_graph.json``).

    Blue nodes  (#6AAFFF) → known in at least one subject.
    Grey nodes  (#999999) → referenced in edges only.

    Returns the path to the generated HTML file.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    merged_path = os.path.join(base_dir, "global_kg", "merged_graph.json")

    if not os.path.exists(merged_path):
        raise FileNotFoundError(f"Global KG not found: {merged_path}")

    with open(merged_path, "r", encoding="utf-8") as f:
        relationships = json.load(f)

    # Build a lookup: node name → subject (used for colouring)
    subjects_dir = os.path.join(base_dir, "subjects")
    subject_map: dict[str, str] = {}
    for subject in os.listdir(subjects_dir):
        nodes = load_subject_nodes(subject)
        for node in nodes:
            subject_map[node] = subject

    output_path = "global_graph.html"
    net = _make_network(height="800px")

    for edge in relationships:
        src = edge["source"]
        tgt = edge["target"]

        for node in (src, tgt):
            if node not in net.get_nodes():
                color = "#6AAFFF" if node in subject_map else "#999999"
                net.add_node(node, label=node, size=16, color=color)

        net.add_edge(src, tgt, title=edge.get("relation", ""))

    net.save_graph(output_path)
    inject_js_into_html(output_path)
    return output_path
