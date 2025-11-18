import streamlit as st
import json
import difflib
from pathlib import Path
import pandas as pd

# ======================================
# PAGE SETUP
# ======================================
st.set_page_config(page_title="📚 Node List & Duplicate Finder", layout="wide")
st.title("📚 Knowledge Graph — Node List & Duplicate Finder")

# subjects directory is 2 levels above /pages/
BASE_DIR = Path(__file__).resolve().parents[2] / "subjects"

if not BASE_DIR.exists():
    st.error(f"❌ subjects directory not found at: {BASE_DIR}")
    st.stop()

# ======================================
# LOAD SUBJECT LIST
# ======================================
subjects = sorted([s for s in BASE_DIR.iterdir() if s.is_dir()])
subject_names = [s.name for s in subjects]

st.sidebar.header("Subjects")
subject_choice = st.sidebar.selectbox("Choose subject:", subject_names)

# Selected subject path
subject_dir = BASE_DIR / subject_choice
edges_file = subject_dir / "relationships" / "matrix_edges.json"

st.subheader(f"📌 Subject: **{subject_choice}**")

# ======================================
# CASE 1: NO matrix_edges.json
# ======================================
if not edges_file.exists():
    st.warning(f"⚠️ No matrix_edges.json found for subject: **{subject_choice}**")
    st.info("You may need to generate relationship edges for this subject.")
    st.stop()  # stop this subject's processing but keep UI active

# ======================================
# CASE 2: matrix_edges.json EXISTS → load normally
# ======================================
with open(edges_file, "r", encoding="utf-8") as f:
    edges = json.load(f)

# Extract unique node names
nodes = sorted({e["source"] for e in edges} | {e["target"] for e in edges})

st.write(f"Total nodes: **{len(nodes)}**")
st.dataframe(pd.DataFrame({"Node Name": nodes}), use_container_width=True)

st.divider()

# ======================================
# DUPLICATE DETECTION (within subject)
# ======================================
st.header("🔎 Duplicate Node Detection")

similarity_threshold = st.slider(
    "Fuzzy match threshold (0.0 = loose, 1.0 = strict)",
    0.1, 1.0, 0.75
)

duplicate_groups = []
checked = set()

for node in nodes:
    if node in checked:
        continue
    matches = difflib.get_close_matches(node, nodes, n=10, cutoff=similarity_threshold)
    group = [m for m in matches if m != node]
    if group:
        duplicate_groups.append([node] + group)
        checked.update(group)

# Display duplicates
if duplicate_groups:
    st.success(f"Found **{len(duplicate_groups)}** duplicate/similar groups.")
else:
    st.info("No duplicates detected with the current threshold.")

for group in duplicate_groups:
    st.markdown("### 🔁 Possible Duplicate Group")
    st.write(group)
    st.markdown("---")

# ======================================
# OPTIONAL — CROSS-SUBJECT CHECK
# ======================================
st.header("🌍 Cross-subject Duplicate Finder")

if st.checkbox("Enable cross-subject check"):
    all_nodes_global = {}

    # Load all subjects
    for subject in subjects:
        path = subject / "relationships" / "matrix_edges.json"
        if not path.exists():
            continue  # skip subjects with no edges
        with open(path, "r", encoding="utf-8") as f:
            ed = json.load(f)
            names = sorted({e["source"] for e in ed} | {e["target"] for e in ed})
            all_nodes_global[subject.name] = names

    flattened = []
    for subj, lst in all_nodes_global.items():
        for node in lst:
            flattened.append((subj, node))

    cross_dups = []
    for i, (subjA, nodeA) in enumerate(flattened):
        for subjB, nodeB in flattened[i + 1:]:
            if subjA == subjB:
                continue
            if difflib.SequenceMatcher(None, nodeA, nodeB).ratio() >= similarity_threshold:
                cross_dups.append((subjA, nodeA, subjB, nodeB))

    if cross_dups:
        st.success(f"Found **{len(cross_dups)}** cross-subject duplicates.")
        df = pd.DataFrame(cross_dups, columns=["Subject A", "Node A", "Subject B", "Node B"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No cross-subject duplicates detected.")
