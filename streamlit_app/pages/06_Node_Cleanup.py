import streamlit as st
import json
from pathlib import Path
import difflib
import networkx as nx

from utils.loaders import (
    list_subjects,
    load_subject_nodes,
    load_relationships,
)
from utils.file_reader import read_markdown

# ===========================================
# CONFIG
# ===========================================
st.set_page_config(page_title="🧹 Node Cleanup", layout="wide")
st.title("🧹 Knowledge Graph — Node Cleanup & QA")

BASE_DIR = Path(__file__).resolve().parents[1]

# ===========================================
# SELECT SUBJECT
# ===========================================
subjects = list_subjects()
if not subjects:
    st.error("No subjects found in /subjects directory.")
    st.stop()

subject = st.selectbox("Select subject:", subjects)

SUBJECT_DIR = BASE_DIR / "subjects" / subject
REL_FILE = SUBJECT_DIR / "relationships" / "matrix_edges.json"
MERGE_LOG = SUBJECT_DIR / "merge_log.txt"

# ===========================================
# LOAD GRAPH
# ===========================================
try:
    node_paths = load_subject_nodes(subject)
except Exception as e:
    st.error(f"Error loading nodes: {e}")
    st.stop()

try:
    relationships = load_relationships(subject)
except Exception as e:
    st.error(f"Error loading edges: {e}")
    st.stop()

# ===========================================
# BUILD GRAPH (nodes from markdown)
# ===========================================
G = nx.DiGraph()

for node_name, md_path in node_paths.items():
    raw = read_markdown(md_path)
    lines = raw.split("\n")

    meta = dict(domain=None, definition=None, description=None, properties={})

    # Simple metadata extraction
    for line in lines:
        if line.startswith("Domain:"):
            meta["domain"] = line.replace("Domain:", "").strip()
        elif line.startswith("Definition:"):
            meta["definition"] = line.replace("Definition:", "").strip()
        elif not meta["description"] and "." in line:
            meta["description"] = line.strip()

    G.add_node(node_name, **meta)

# add edges
for e in relationships:
    s = e.get("source")
    t = e.get("target")
    if s in G and t in G:
        G.add_edge(s, t, type=e.get("type", "related_to"))

# ===========================================
# HELPERS
# ===========================================
def find_incomplete_nodes(graph):
    """
    Incomplete = missing ALL metadata fields.
    """
    incomplete = []
    for node, props in graph.nodes(data=True):
        if not props.get("domain") and not props.get("definition") and not props.get("description"):
            incomplete.append(node)
    return sorted(incomplete)

def find_complete_nodes(graph):
    complete = []
    for node, props in graph.nodes(data=True):
        if props.get("domain") or props.get("definition") or props.get("description"):
            complete.append(node)
    return sorted(complete)

def suggest_merges(node, all_nodes):
    return difflib.get_close_matches(node, all_nodes, n=5, cutoff=0.3)

def save_subject_graph(subject, graph_data):
    out_file = SUBJECT_DIR / "relationships" / "matrix_edges.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    st.success("💾 Graph saved!")

def merge_nodes(graph_edges, old_node, new_node):
    """
    Merge incomplete → existing node.
    Only touches edges; node metadata is stored in markdown.
    """

    # Redirect all edges
    for e in graph_edges:
        if e["source"] == old_node:
            e["source"] = new_node
        if e["target"] == old_node:
            e["target"] = new_node

    # Log
    with open(MERGE_LOG, "a", encoding="utf-8") as f:
        f.write(f"Merged {old_node} → {new_node}\n")

    return graph_edges

# ===========================================
# COMPLETE NODES
# ===========================================
st.header("✅ Complete Nodes")
complete_nodes = find_complete_nodes(G)

st.write(f"Found **{len(complete_nodes)}** complete nodes.")
st.dataframe({"Complete Nodes": complete_nodes})

st.download_button(
    "⬇️ Download Complete Nodes",
    data=json.dumps(complete_nodes, indent=2),
    file_name=f"{subject}_complete_nodes.json"
)

st.divider()

# ===========================================
# INCOMPLETE NODES
# ===========================================
st.header("⚠️ Incomplete Nodes")
incomplete_nodes = find_incomplete_nodes(G)

st.write(f"Found **{len(incomplete_nodes)}** incomplete nodes.")
st.dataframe({"Incomplete Nodes": incomplete_nodes})

st.download_button(
    "⬇️ Download Incomplete Nodes",
    data=json.dumps(incomplete_nodes, indent=2),
    file_name=f"{subject}_incomplete_nodes.json"
)

st.divider()

# ===========================================
# MERGE TOOL
# ===========================================
st.header("🔧 Fix / Merge Incomplete Nodes")

col1, col2 = st.columns(2)

with col1:
    old_node = st.selectbox("Incomplete node:", [""] + incomplete_nodes)

with col2:
    all_nodes = sorted(list(G.nodes()))
    new_node = st.selectbox("Merge into:", [""] + all_nodes)

# Suggestions
if old_node:
    st.subheader(f"🔍 Suggestions for `{old_node}`:")
    suggestions = suggest_merges(old_node, all_nodes)
    if suggestions:
        st.info("Possible merges:")
        st.write(suggestions)
    else:
        st.warning("No close matches found.")

# ===========================================
# APPLY MERGE
# ===========================================
if st.button("🚀 Merge Now"):
    if not old_node or not new_node:
        st.warning("Select both nodes.")
    elif old_node == new_node:
        st.warning("Cannot merge a node into itself.")
    else:
        # Load raw edges JSON
        with open(REL_FILE, "r", encoding="utf-8") as f:
            graph_edges = json.load(f)

        updated_edges = merge_nodes(graph_edges, old_node, new_node)
        save_subject_graph(subject, updated_edges)

        st.success(f"Merged `{old_node}` → `{new_node}`")
        st.rerun()
