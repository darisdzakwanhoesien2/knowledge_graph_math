import sys
import os
import streamlit as st
from utils.file_reader import read_markdown

# =========================================================
# Fix Python Path
# =========================================================
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ROOT = os.path.abspath(os.path.join(BASE, '..'))
sys.path.append(BASE)
sys.path.append(ROOT)

# =========================================================
# Page Config
# =========================================================
st.set_page_config(layout="wide")
st.title("📘 Subject Browser")

# =========================================================
# Read URL Parameters
# =========================================================
params = st.query_params
url_subject = params.get("subject", None)
url_node = params.get("node", None)

# sync to session state
if url_subject and st.session_state.get("sb_subject") != url_subject:
    st.session_state["sb_subject"] = url_subject

if url_node and st.session_state.get("sb_node") != url_node:
    st.session_state["sb_node"] = url_node

subject = st.session_state.get("sb_subject", url_subject)
node = st.session_state.get("sb_node", url_node)

# =========================================================
# Helper functions
# =========================================================
def list_subjects():
    subjects_dir = os.path.join(ROOT, "subjects")
    return sorted([
        d for d in os.listdir(subjects_dir)
        if os.path.isdir(os.path.join(subjects_dir, d))
    ])

def list_nodes(subject):
    node_dir = os.path.join(ROOT, "subjects", subject, "nodes")
    if not os.path.isdir(node_dir):
        return []
    return sorted(f[:-3] for f in os.listdir(node_dir) if f.endswith(".md"))

# =========================================================
# Subject + Node UI
# =========================================================
subjects = list_subjects()

if not subjects:
    st.error("❌ No subjects found.")
    st.stop()

subject = st.selectbox(
    "Select subject:",
    subjects,
    index=subjects.index(subject) if subject in subjects else 0
)
st.session_state["sb_subject"] = subject

nodes = list_nodes(subject)
if not nodes:
    st.error(f"❌ No nodes found in subject: {subject}")
    st.stop()

node = st.selectbox(
    "Select node:",
    nodes,
    index=nodes.index(node) if node in nodes else 0
)
st.session_state["sb_node"] = node

# update query params without switching pages
st.query_params["subject"] = subject
st.query_params["node"] = node

# =========================================================
# Load Markdown
# =========================================================
md_path = os.path.join(ROOT, "subjects", subject, "nodes", f"{node}.md")

st.markdown("---")
st.markdown(f"## 📄 {node}")

if not os.path.exists(md_path):
    st.error(f"❌ Markdown file not found:\n{md_path}")
else:
    st.markdown(read_markdown(md_path), unsafe_allow_html=True)

# =========================================================
# Extract basic metadata
# =========================================================
def get_meta(md):
    meta = {"Type": None, "Domain": None, "Prereq": [], "Related": []}
    for line in md.split("\n"):
        line = line.strip()
        if line.startswith("Type:"):
            meta["Type"] = line.replace("Type:", "").strip()
        elif line.startswith("Domain:"):
            meta["Domain"] = line.replace("Domain:", "").strip()
        elif line.startswith("Prerequisites:"):
            raw = line.replace("Prerequisites:", "").strip()
            meta["Prereq"] = [x.strip() for x in raw.split(",")] if raw else []
        elif line.startswith("Related Nodes:"):
            raw = line.replace("Related Nodes:", "").strip()
            meta["Related"] = [x.strip() for x in raw.split(",")] if raw else []
    return meta

if os.path.exists(md_path):
    meta = get_meta(read_markdown(md_path))

    st.markdown("---")
    st.subheader("📦 Metadata")

    st.write(f"**Type:** {meta['Type'] or '(none)'}")
    st.write(f"**Domain:** {meta['Domain'] or '(none)'}")

    st.write("**Prerequisites:**")
    if meta["Prereq"]:
        for p in meta["Prereq"]:
            st.markdown(f"- {p}")
    else:
        st.caption("*(none)*")

    st.write("**Related:**")
    if meta["Related"]:
        for r in meta["Related"]:
            st.markdown(f"- {r}")
    else:
        st.caption("*(none)*")
