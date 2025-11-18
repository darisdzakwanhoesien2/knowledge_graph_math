import streamlit as st
import json
from pathlib import Path

from utils.loaders import list_subjects, load_subject_nodes, load_relationships

# =======================================================
# CONFIG
# =======================================================
st.set_page_config(page_title="🔗 Edge Explorer", layout="wide")
st.title("🔗 Subject Relationship Explorer & Editor")

BASE_DIR = Path(__file__).resolve().parents[1]

# =======================================================
# SELECT SUBJECT
# =======================================================
subjects = list_subjects()
if not subjects:
    st.error("No subjects found.")
    st.stop()

subject = st.selectbox("Select subject:", subjects)

SUBJECT_DIR = BASE_DIR / "subjects" / subject
EDGE_FILE = SUBJECT_DIR / "relationships" / "matrix_edges.json"

# =======================================================
# LOAD RELATIONSHIPS
# =======================================================
try:
    edges = load_relationships(subject)
except Exception as e:
    st.error(f"Failed to load matrix_edges.json: {e}")
    st.stop()

# =======================================================
# LOAD SUBJECT NODES
# =======================================================
subject_node_paths = load_subject_nodes(subject)
subject_nodes = sorted(subject_node_paths.keys())

# =======================================================
# CREATE FULL NODE LIST (subject nodes + nodes from edges)
# =======================================================
edge_nodes = sorted(
    set([e["source"] for e in edges] + [e["target"] for e in edges])
)

# Nodes that appear in edges but don't exist in subject
missing_nodes = sorted(set(edge_nodes) - set(subject_nodes))

# Full selectable list
all_nodes = sorted(set(subject_nodes + missing_nodes))

# Label missing nodes clearly
def node_label(node):
    return node + ("  ❗" if node in missing_nodes else "")

labelled_nodes = [node_label(n) for n in all_nodes]

# Helper to get index safely
def safe_index(node):
    try:
        return all_nodes.index(node)
    except ValueError:
        return 0  # fallback to first element


# =======================================================
# FILTERS
# =======================================================
st.subheader("🔍 Filter Edges")

col1, col2, col3 = st.columns(3)

with col1:
    f_source = st.selectbox(
        "Filter by source:",
        ["All"] + labelled_nodes,
        index=0
    )
with col2:
    f_target = st.selectbox(
        "Filter by target:",
        ["All"] + labelled_nodes,
        index=0
    )
with col3:
    f_relation = st.text_input("Filter by relation (contains):", "")

def e_match(e):
    src_lbl = node_label(e["source"])
    tgt_lbl = node_label(e["target"])
    if f_source != "All" and src_lbl != f_source:
        return False
    if f_target != "All" and tgt_lbl != f_target:
        return False
    if f_relation and f_relation.lower() not in e["relation"].lower():
        return False
    return True

filtered_edges = [e for e in edges if e_match(e)]


# =======================================================
# DISPLAY / EDIT EDGES
# =======================================================
st.subheader(f"📌 Showing {len(filtered_edges)} relationship(s)")

for idx, e in enumerate(filtered_edges):

    st.markdown(f"### Edge {idx+1}")
    colA, colB, colC, colD = st.columns([3, 3, 3, 1])

    with colA:
        src = st.selectbox(
            f"Source ({idx})",
            labelled_nodes,
            index=safe_index(e["source"]),
            key=f"src_{idx}"
        )
        src = src.replace(" ❗", "")

    with colB:
        tgt = st.selectbox(
            f"Target ({idx})",
            labelled_nodes,
            index=safe_index(e["target"]),
            key=f"tgt_{idx}"
        )
        tgt = tgt.replace(" ❗", "")

    with colC:
        rel = st.text_input(f"Relation ({idx})", e["relation"], key=f"rel_{idx}")

    with colD:
        if st.button("❌", key=f"del_{idx}"):
            edges.remove(e)
            with open(EDGE_FILE, "w", encoding="utf-8") as f:
                json.dump(edges, f, indent=2, ensure_ascii=False)
            st.success("Edge deleted.")
            st.rerun()

    # Apply edits to the edge
    e["source"] = src
    e["target"] = tgt
    e["relation"] = rel

st.markdown("---")


# =======================================================
# ADD NEW EDGE
# =======================================================
st.subheader("➕ Add New Relationship")

col1, col2, col3 = st.columns(3)

with col1:
    n_src = st.selectbox("Source", labelled_nodes, key="new_src")
    n_src = n_src.replace(" ❗", "")

with col2:
    n_tgt = st.selectbox("Target", labelled_nodes, key="new_tgt")
    n_tgt = n_tgt.replace(" ❗", "")

with col3:
    n_rel = st.text_input("Relation", key="new_rel")

if st.button("Add Edge"):
    if not n_src or not n_tgt or not n_rel:
        st.warning("All fields required.")
    else:
        edges.append({"source": n_src, "target": n_tgt, "relation": n_rel})
        with open(EDGE_FILE, "w", encoding="utf-8") as f:
            json.dump(edges, f, indent=2, ensure_ascii=False)
        st.success("Edge added.")
        st.rerun()

st.markdown("---")

# =======================================================
# SAVE ALL
# =======================================================
if st.button("💾 Save All Changes"):
    try:
        with open(EDGE_FILE, "w", encoding="utf-8") as f:
            json.dump(edges, f, indent=2, ensure_ascii=False)
        st.success("Changes saved.")
    except Exception as e:
        st.error(f"Failed to save: {e}")

st.info("Missing nodes are marked with ❗ — consider creating Markdown files for them.")
