import os
import json
from pyvis.network import Network
from utils.loaders import load_relationships, load_subject_nodes


# ============================================================================
# Helper: Inject custom JS into PyVis HTML to make nodes clickable
# ============================================================================
def inject_click_js(html_file):

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    custom_js = """
    <script>
    // When a node is clicked, redirect to its URL
    network.on("click", function(params) {
        if (params.nodes.length > 0) {
            var nodeId = params.nodes[0];
            var node = network.body.data.nodes.get(nodeId);

            // Extract URL stored in node's 'title' via <a href="...">
            var div = document.createElement('div');
            div.innerHTML = node.title;
            var link = div.querySelector('a');

            if (link && link.href) {
                window.parent.location.href = link.href;
            }
        }
    });
    </script>
    """

    # Insert JS before </body>
    html = html.replace("</body>", custom_js + "\n</body>")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)


# ============================================================================
# Helper: Create HTML link for tooltip (title), label stays clean text
# ============================================================================
def make_clickable_title(node_name, subject):
    """
    Returns HTML <a> that PyVis will show in the tooltip.
    The JavaScript click handler extracts this URL.
    """
    url = f"/Subject_Browser?subject={subject}&node={node_name}"
    return f'<a href="{url}" target="_parent">Open {node_name}</a>'


# ============================================================================
# Build Subject Graph (auto-add missing nodes)
# ============================================================================
def build_subject_graph(subject):

    nodes = load_subject_nodes(subject)
    relationships = load_relationships(subject)

    output_path = f"{subject}_graph.html"

    # Build PyVis network
    net = Network(
        height="750px",
        width="100%",
        directed=True,
        bgcolor="#202020",
        font_color="white"
    )

    net.force_atlas_2based(gravity=-50)

    # ----------------------------------------------------------
    # 1. Add existing nodes (clean label, clickable tooltip)
    # ----------------------------------------------------------
    for node_name in nodes.keys():

        net.add_node(
            node_name,
            label=node_name,                                # clean readable label
            title=make_clickable_title(node_name, subject), # HTML link in tooltip
            shape="dot",
            size=18,
            color="#6AAFFF",  # blue = real node
        )

    # ----------------------------------------------------------
    # 2. Add missing nodes (gray, not clickable)
    # ----------------------------------------------------------
    for edge in relationships:
        src = edge["source"]
        tgt = edge["target"]

        if src not in net.get_nodes():
            net.add_node(
                src,
                label=src,
                title=f"{src} (missing node file)",
                shape="dot",
                size=14,
                color="#888888",
            )

        if tgt not in net.get_nodes():
            net.add_node(
                tgt,
                label=tgt,
                title=f"{tgt} (missing node file)",
                shape="dot",
                size=14,
                color="#888888",
            )

    # ----------------------------------------------------------
    # 3. Add edges
    # ----------------------------------------------------------
    for edge in relationships:
        net.add_edge(
            edge["source"],
            edge["target"],
            title=edge.get("relation", "")
        )

    # Save graph
    net.save_graph(output_path)

    # Add JavaScript click handler
    inject_click_js(output_path)

    return output_path


# ============================================================================
# Build Global Graph (cross-subject)
# ============================================================================
def build_global_graph():

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    merged_path = os.path.join(base_dir, "global_kg", "merged_graph.json")

    if not os.path.exists(merged_path):
        raise FileNotFoundError(f"Global KG not found: {merged_path}")

    with open(merged_path, "r") as f:
        edges = json.load(f)

    output_path = "global_graph.html"

    # Construct global PyVis network
    net = Network(
        height="850px",
        width="100%",
        directed=True,
        bgcolor="#202020",
        font_color="white"
    )

    net.force_atlas_2based(gravity=-50)

    # ----------------------------------------------------------
    # Map node → subject to enable cross-subject navigation
    # ----------------------------------------------------------
    subjects_dir = os.path.join(base_dir, "subjects")
    subject_map = {}

    for subject in os.listdir(subjects_dir):
        subnodes = load_subject_nodes(subject)
        for n in subnodes.keys():
            subject_map[n] = subject

    # ----------------------------------------------------------
    # Add nodes for global graph
    # ----------------------------------------------------------
    for edge in edges:
        src = edge["source"]
        tgt = edge["target"]

        # Add source node
        if src not in net.get_nodes():
            if src in subject_map:
                title = make_clickable_title(src, subject_map[src])
                color = "#6AAFFF"
            else:
                title = f"{src} (missing node file)"
                color = "#888888"

            net.add_node(src, label=src, title=title, color=color)

        # Add target node
        if tgt not in net.get_nodes():
            if tgt in subject_map:
                title = make_clickable_title(tgt, subject_map[tgt])
                color = "#6AAFFF"
            else:
                title = f"{tgt} (missing node file)"
                color = "#888888"

            net.add_node(tgt, label=tgt, title=title, color=color)

        # Add edge
        net.add_edge(src, tgt)

    # Save & inject JS
    net.save_graph(output_path)
    inject_click_js(output_path)

    return output_path
