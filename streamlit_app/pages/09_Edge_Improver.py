import streamlit as st
import json
import difflib
import pandas as pd
from pathlib import Path
from datetime import datetime

# ============================================================
# PAGE SETTINGS
# ============================================================
st.set_page_config(page_title="🔧 Edge Improver", layout="wide")
st.title("🔧 Knowledge Graph — Edge Improvement & QA")

BASE_DIR = Path(__file__).resolve().parents[2] / "subjects"
LOG_FILE = Path(__file__).resolve().parents[2] / "edge_log.txt"

if not BASE_DIR.exists():
    st.error(f"❌ subjects directory not found: {BASE_DIR}")
    st.stop()

# ============================================================
# SUBJECT DROPDOWN
# ============================================================
subjects = sorted([s.name for s in BASE_DIR.iterdir() if s.is_dir()])
subject_choice = st.sidebar.selectbox("Select Subject", subjects)

subject_path = BASE_DIR / subject_choice / "relationships"
edges_path = subject_path / "matrix_edges.json"

st.subheader(f"📘 Subject: **{subject_choice}**")

if not edges_path.exists():
    st.warning(f"⚠️ This subject has no matrix_edges.json: {edges_path}")
    st.stop()

# ============================================================
# LOAD + NORMALIZE EDGES
# ============================================================
with open(edges_path, "r", encoding="utf-8") as f:
    edges = json.load(f)

# Normalize `relation` field
for e in edges:
    if "relation" not in e:
        if "type" in e:
            e["relation"] = e["type"]
        else:
            e["relation"] = "related_to"

df = pd.DataFrame(edges)
st.write(f"Loaded **{len(edges)}** edges.")

st.dataframe(df, use_container_width=True)

st.divider()

# ============================================================
# 1. DUPLICATE EDGE DETECTION
# ============================================================
st.header("🔍 Duplicate Edge Detection")

duplicate_edges = []
seen = set()

for e in edges:
    t = (e["source"], e["target"], e["relation"])
    if t in seen:
        duplicate_edges.append(e)
    else:
        seen.add(t)

if duplicate_edges:
    st.error(f"Found **{len(duplicate_edges)}** exact duplicate edges.")
    st.write(duplicate_edges)
else:
    st.success("No exact duplicate edges found.")

st.divider()

# ============================================================
# 2. NEAR-DUPLICATE RELATIONS
# ============================================================
st.header("🧠 Near-Duplicate Relations (Fuzzy Match)")

relation_names = sorted({e["relation"] for e in edges})
groups = []

threshold = st.slider("Match sensitivity", 0.5, 0.99, 0.75)

used = set()
for r in relation_names:
    if r in used:
        continue
    matches = difflib.get_close_matches(r, relation_names, n=10, cutoff=threshold)
    group = [m for m in matches if m != r]
    if group:
        groups.append([r] + group)
        used.update(group)

if groups:
    st.warning("These relations are probably duplicates / inconsistent:")
    for g in groups:
        st.write("→ ", g)
else:
    st.success("No near-duplicate relation names found.")

st.divider()

# ============================================================
# 3. EDIT / FIX RELATIONS
# ============================================================
st.header("✏️ Edit / Fix Relations")

all_relations = sorted(list(set(df["relation"])))

col1, col2, col3 = st.columns(3)

with col1:
    selected_source = st.selectbox("Source Node", sorted(df["source"].unique()))

with col2:
    selected_target = st.selectbox("Target Node", sorted(df["target"].unique()))

with col3:
    selected_relation = st.selectbox("Relation", all_relations)

filtered = df[
    (df["source"] == selected_source)
    & (df["target"] == selected_target)
    & (df["relation"] == selected_relation)
]

st.write("Matching edges:", filtered)

new_relation = st.text_input("New Relation Name (optional)", value=selected_relation)

if st.button("💾 Update Relation"):
    for e in edges:
        if (
            e["source"] == selected_source and
            e["target"] == selected_target and
            e["relation"] == selected_relation
        ):
            e["relation"] = new_relation

    with open(edges_path, "w", encoding="utf-8") as f:
        json.dump(edges, f, indent=2)

    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} UPDATED: {selected_source} → {selected_target}: '{selected_relation}' → '{new_relation}'\n")

    st.success("Relation updated!")
    st.rerun()

st.divider()

# ============================================================
# 4. ADD NEW EDGE
# ============================================================
st.header("➕ Add New Edge")

colA, colB, colC = st.columns(3)

with colA:
    add_src = st.text_input("Source")

with colB:
    add_tgt = st.text_input("Target")

with colC:
    add_rel = st.text_input("Relation")

if st.button("➕ Add Edge"):
    if add_src and add_tgt and add_rel:
        new_edge = {"source": add_src, "target": add_tgt, "relation": add_rel}
        edges.append(new_edge)

        with open(edges_path, "w", encoding="utf-8") as f:
            json.dump(edges, f, indent=2)

        with open(LOG_FILE, "a") as log:
            log.write(f"{datetime.now()} ADDED: {new_edge}\n")

        st.success("Edge added!")
        st.rerun()
    else:
        st.warning("Fill all fields!")

st.divider()

# ============================================================
# 5. DELETE EDGE
# ============================================================
st.header("🗑️ Delete Edge")

del_idx = st.number_input(
    "Index to delete (0-based)", 
    min_value=0, max_value=len(edges)-1, step=1
)

if st.button("🗑 Delete Edge"):
    removed = edges.pop(del_idx)

    with open(edges_path, "w", encoding="utf-8") as f:
        json.dump(edges, f, indent=2)

    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} DELETED: {removed}\n")

    st.success(f"Deleted: {removed}")
    st.rerun()
