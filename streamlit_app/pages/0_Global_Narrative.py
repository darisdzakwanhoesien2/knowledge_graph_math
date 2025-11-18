import streamlit as st
import json
from pathlib import Path
import networkx as nx
import itertools
import pandas as pd
from datetime import datetime

# Utils
from utils.file_reader import read_markdown
from utils.loaders import list_subjects, load_subject_nodes, load_relationships

# Try Louvain
try:
    import community as community_louvain
    _LOUVAIN_AVAILABLE = True
except Exception:
    _LOUVAIN_AVAILABLE = False

st.set_page_config(page_title="📖 Global Narrative", layout="wide")
st.title("📖 Global Narrative — Auto-generated Chapter Overviews")

# --------------------------------------------------------------
# SUBJECT SELECTION DROPDOWN
# --------------------------------------------------------------
st.sidebar.header("Dataset")
subjects = list_subjects()

if not subjects:
    st.error("No subjects found inside /subjects directory.")
    st.stop()

subject = st.sidebar.selectbox("Select subject graph:", subjects)

# --------------------------------------------------------------
# LOAD NODES + RELATIONSHIPS FOR THIS SUBJECT
# --------------------------------------------------------------
try:
    node_paths = load_subject_nodes(subject)
except Exception as e:
    st.error(f"Error loading nodes for subject '{subject}': {e}")
    st.stop()

try:
    relationships = load_relationships(subject)
except Exception as e:
    st.error(f"Error loading relationships for subject '{subject}': {e}")
    st.stop()

# --------------------------------------------------------------
# BUILD GRAPH
# --------------------------------------------------------------
G = nx.DiGraph()

# Add nodes (metadata comes from markdown)
for node_name, md_path in node_paths.items():
    raw_text = read_markdown(md_path)

    # Extract metadata from markdown headers
    meta = {"definition": "", "description": ""}
    for line in raw_text.split("\n"):
        if line.startswith("Type:"):
            meta["type"] = line.replace("Type:", "").strip()
        elif line.startswith("Domain:"):
            meta["domain"] = line.replace("Domain:", "").strip()

        # simple definition extraction
        if not meta.get("definition"):
            if "." in line:
                meta["definition"] = line.strip()

    G.add_node(node_name, **meta)

# Add edges
for edge in relationships:
    s = edge.get("source")
    t = edge.get("target")

    if s in G and t in G:
        G.add_edge(s, t, type=edge.get("type", "related_to"))

if G.number_of_nodes() == 0:
    st.warning("This subject contains no graph data.")
    st.stop()

# --------------------------------------------------------------
# SIDEBAR OPTIONS
# --------------------------------------------------------------
st.sidebar.header("Clustering Options")

algo_options = []
if _LOUVAIN_AVAILABLE:
    algo_options.append("Louvain Modularity (recommended)")
algo_options += [
    "Greedy Modularity",
    "Label Propagation",
    "Girvan-Newman (edge betweenness)"
]

algorithm = st.sidebar.selectbox("Clustering algorithm:", algo_options)
max_chapters = st.sidebar.slider("Max chapters", 1, 50, 12)
include_examples = st.sidebar.checkbox("Include short examples", True)
compute_centrality = st.sidebar.checkbox("Compute centrality metrics", True)
gn_levels = st.sidebar.slider("Girvan-Newman levels", 1, 3, 1)

st.info(f"Generating narrative for **{subject}** …")

# --------------------------------------------------------------
# CLUSTERING HELPERS
# --------------------------------------------------------------
@st.cache_data(ttl=3600)
def _run_louvain(_graph):
    part = community_louvain.best_partition(_graph.to_undirected())
    clusters = {}
    for n, c in part.items():
        clusters.setdefault(c, []).append(n)
    return {k: sorted(v) for k, v in clusters.items()}

@st.cache_data(ttl=3600)
def _run_greedy(_graph):
    und = _graph.to_undirected()
    comms = list(nx.algorithms.community.greedy_modularity_communities(und))
    return {i: sorted(list(c)) for i, c in enumerate(comms)}

@st.cache_data(ttl=3600)
def _run_label_prop(_graph):
    und = _graph.to_undirected()
    comms = list(nx.algorithms.community.label_propagation_communities(und))
    return {i: sorted(list(c)) for i, c in enumerate(comms)}

@st.cache_data(ttl=3600)
def _run_girvan(_graph, _levels=1):
    und = _graph.to_undirected()
    comp = nx.algorithms.community.girvan_newman(und)
    limited = list(itertools.islice(comp, _levels))
    if not limited:
        return {}
    part = limited[-1]
    return {i: sorted(list(c)) for i, c in enumerate(part)}

# --------------------------------------------------------------
# RUN CLUSTERING
# --------------------------------------------------------------
with st.spinner("Running clustering..."):
    if algorithm.startswith("Louvain"):
        clusters = _run_louvain(G)
    elif algorithm == "Greedy Modularity":
        clusters = _run_greedy(G)
    elif algorithm == "Label Propagation":
        clusters = _run_label_prop(G)
    elif algorithm.startswith("Girvan-Newman"):
        clusters = _run_girvan(G, _levels=gn_levels)
    else:
        st.error("Unknown algorithm.")
        st.stop()

if not clusters:
    st.warning("No clusters found.")
    st.stop()

# --------------------------------------------------------------
# CENTRALITY
# --------------------------------------------------------------
pagerank = {}
degree = dict(G.degree())

if compute_centrality:
    try:
        pagerank = nx.pagerank(G)
    except:
        pagerank = {n: 0.0 for n in G.nodes()}

# --------------------------------------------------------------
# CLUSTER SUMMARY + NARRATIVE GENERATION
# --------------------------------------------------------------
def cluster_title_info(members):
    avg_deg = sum(degree.get(m, 0) for m in members) / (len(members) or 1)
    avg_pr = sum(pagerank.get(m, 0.0) for m in members) / (len(members) or 1)
    sorted_members = sorted(members, key=lambda n: (-degree.get(n, 0), -pagerank.get(n, 0)))
    return (avg_deg + avg_pr), sorted_members[0], sorted_members

cluster_infos = []
for cid, members in clusters.items():
    score, title, sorted_members = cluster_title_info(members)
    cluster_infos.append({
        "cluster_id": cid,
        "members": members,
        "size": len(members),
        "score": score,
        "title": title,
        "top": sorted_members[:8],
    })

cluster_infos_sorted = sorted(cluster_infos, key=lambda x: (-x["size"], -x["score"]))
cluster_infos_sorted = cluster_infos_sorted[:max_chapters]

# --------------------------------------------------------------
# BUILD NARRATIVE
# --------------------------------------------------------------
def make_chapter(info):
    title = info["title"]
    members = info["members"]
    top = info["top"]

    examples = []
    if include_examples:
        for m in top[:3]:
            descr = G.nodes[m].get("definition") or G.nodes[m].get("description") or ""
            if descr:
                examples.append(f"**{m}** — {descr.split('.')[0]}.")

    lines = []
    lines.append(f"### Chapter {info['cluster_id']+1}: {title}")
    lines.append(f"- **Concepts:** {len(members)} total")
    lines.append(f"- **Key ideas:** {', '.join(top[:6])}")

    if examples:
        lines.append("- **Examples:**")
        for e in examples:
            lines.append(f"  - {e}")

    return "\n".join(lines)


# --------------------------------------------------------------
# RENDER OUTPUT
# --------------------------------------------------------------
full_md = "# Global Narrative\n"
full_md += f"*Subject: **{subject}***\n\n"

full_md += "## Chapters\n"
for info in cluster_infos_sorted:
    full_md += make_chapter(info) + "\n\n"

st.header("Generated Narrative")
st.markdown(full_md, unsafe_allow_html=True)

# --------------------------------------------------------------
# DOWNLOAD
# --------------------------------------------------------------
st.download_button(
    "⬇️ Download Narrative (Markdown)",
    data=full_md,
    file_name=f"{subject}_narrative.md",
    mime="text/markdown"
)
