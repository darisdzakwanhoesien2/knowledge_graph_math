import os
import json
from pyvis.network import Network
from utils.loaders import load_relationships, load_subject_nodes


# ============================================================================
# Inject JS: When clicking PyVis node → update Streamlit query params
# ============================================================================
def inject_click_js(html_file):
    """Inject JS so that clicking a node updates the parent Streamlit URL."""
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    custom_js = """
    <script>
    // Ensure "network" is available
    network.on("click", function(params) {
        if (params.nodes && params.nodes.length > 0) {
            const nodeId = params.nodes[0];

            // Update the parent URL without reloading iframe
            const parent = window.parent;
            const base = parent.location.origin + parent.location.pathname;
            const newUrl = base + "?selected_node=" + encodeURIComponent(nodeId);

            parent.history.replaceState(null, "", newUrl);
        }
    });
    </script>
    """

    # Insert BEFORE </body>
    html = html.replace("</body>", custom_js + "\n</body>")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)



# ============================================================================
# Build Subject Graph
# ============================================================================
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

    net.force_atlas_2based(gravity=-50)

    # 1. Add existing nodes
    for node_name in nodes.keys():
        net.add_node(
            node_name,
            label=node_name,
            title=f"Click to select: {node_name}",
            color="#6AAFFF",
            size=18
        )

    # 2. Add missing nodes
    for edge in relationships:
        for node in [edge["source"], edge["target"]]:
            if node not in net.get_nodes():
                net.add_node(
                    node,
                    label=node,
                    title=f"{node} (missing node file)",
                    color="#999999",
                    size=14
                )

    # 3. Add edges
    for edge in relationships:
        net.add_edge(edge["source"], edge["target"], title=edge.get("relation", ""))

    # Save & inject JS
    net.save_graph(output_path)
    inject_click_js(output_path)

    return output_path


# ============================================================================
# Build Global Graph
# ============================================================================
def build_global_graph():

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    merged_path = os.path.join(base_dir, "global_kg", "merged_graph.json")

    if not os.path.exists(merged_path):
        raise FileNotFoundError(f"Global KG not found: {merged_path}")

    with open(merged_path, "r") as f:
        edges = json.load(f)

    output_path = "global_graph.html"

    net = Network(
        height="850px",
        width="100%",
        directed=True,
        bgcolor="#202020",
        font_color="white",
    )

    net.force_atlas_2based(gravity=-50)

    # Map node → subject
    subjects_dir = os.path.join(base_dir, "subjects")
    subject_map = {}
    for subject in os.listdir(subjects_dir):
        subnodes = load_subject_nodes(subject)
        for n in subnodes.keys():
            subject_map[n] = subject

    # Add nodes
    for edge in edges:
        for node in [edge["source"], edge["target"]]:

            if node not in net.get_nodes():

                # clickable if subject found
                color = "#6AAFFF" if node in subject_map else "#999999"
                title = f"Click to select: {node}"

                net.add_node(
                    node,
                    label=node,
                    title=title,
                    color=color
                )

        net.add_edge(edge["source"], edge["target"])

    # Save & inject JS
    net.save_graph(output_path)
    inject_click_js(output_path)

    return output_path