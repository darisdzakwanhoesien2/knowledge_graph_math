import sys
import os

# =========================================================
# Fix paths (so utils and shared modules always load)
# =========================================================
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ROOT = os.path.abspath(os.path.join(BASE, '..'))

sys.path.append(BASE)    # streamlit_app/
sys.path.append(ROOT)    # project root/

import streamlit as st
from utils.file_reader import read_markdown
from utils.loaders import load_subject_nodes


# =========================================================
# Sync URL → session_state for subject & node
# =========================================================
params = st.query_params

if "subject" in params:
    url_subject = params["subject"]
    if st.session_state.get("sb_subject") != url_subject:
        st.session_state["sb_subject"] = url_subject
        st.rerun()

if "node" in params:
    url_node = params["node"]
    if st.session_state.get("sb_node") != url_node:
        st.session_state["sb_node"] = url_node
        st.rerun()


# =========================================================
# Page Setup
# =========================================================
st.set_page_config(layout="wide")
st.title("📘 Subject Browser")


# =========================================================
# List subjects
# =========================================================
subjects_dir = os.path.join(ROOT, "subjects")

subjects = [
    name
    for name in os.listdir(subjects_dir)
    if os.path.isdir(os.path.join(subjects_dir, name))
]

subjects_sorted = sorted(subjects)

# Default subject
current_subject = st.session_state.get("sb_subject", subjects_sorted[0])

# Sync subject dropdown
current_subject = st.selectbox("Select subject:", subjects_sorted, index=subjects_sorted.index(current_subject))
st.session_state["sb_subject"] = current_subject


# =========================================================
# Load nodes in this subject
# =========================================================
nodes = load_subject_nodes(current_subject)
node_names = sorted(nodes.keys())

if not node_names:
    st.error(f"No nodes found in `{current_subject}`")
    st.stop()


# =========================================================
# Node selection dropdown
# =========================================================
current_node = st.session_state.get("sb_node", node_names[0])

# Validate: if URL node doesn’t exist, fallback
if current_node not in node_names:
    current_node = node_names[0]
    st.session_state["sb_node"] = current_node

# Dropdown UI
current_node = st.selectbox(
    "Select node:",
    node_names,
    index=node_names.index(current_node)
)

# Save into session_state
st.session_state["sb_node"] = current_node

# Update URL dynamically
st.query_params["subject"] = current_subject
st.query_params["node"] = current_node


# =========================================================
# Render the Markdown file
# =========================================================
markdown_path = nodes[current_node]
content = read_markdown(markdown_path)

# Improve section spacing + enable LaTeX
st.markdown(content, unsafe_allow_html=True)


# =========================================================
# Cross-Link Clicking (Optional Extension)
# e.g. clicking Matrix_Norms inside markdown jumps here
# =========================================================
def auto_detect_known_nodes(markdown: str, subject_dir: str):
    """
    Scans markdown for patterns like *Node_Name* or Node_Name and replaces
    them with clickable Streamlit links.
    """
    node_dir = os.path.join(subject_dir, "nodes")
    available = [f.replace(".md", "") for f in os.listdir(node_dir) if f.endswith(".md")]

    for n in available:
        markdown = markdown.replace(
            f"*{n}*",
            f"[{n}](/Subject_Browser?subject={current_subject}&node={n})"
        )
        markdown = markdown.replace(
            f"{n}",
            f"[{n}](/Subject_Browser?subject={current_subject}&node={n})"
        )

    return markdown

# Auto-replace cross-links
# crosslinked = auto_detect_known_nodes(content, os.path.join(subjects_dir, current_subject))
# st.markdown(crosslinked, unsafe_allow_html=True)
