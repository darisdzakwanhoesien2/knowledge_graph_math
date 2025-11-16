import sys
import os

# =========================================================
# Fix paths for imports
# =========================================================
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ROOT = os.path.abspath(os.path.join(BASE, '..'))

sys.path.append(BASE)    # streamlit_app/
sys.path.append(ROOT)    # project root/

# =========================================================
# Imports
# =========================================================
import streamlit as st
from utils.file_reader import read_markdown
from utils.loaders import load_subject_nodes


# =========================================================
# Load URL parameters FIRST
# =========================================================
params = st.query_params

url_subject = params.get("subject", None)
url_node = params.get("node", None)


# =========================================================
# Page Config
# =========================================================
st.set_page_config(layout="wide")
st.title("📘 Subject Browser")


# =========================================================
# Load all available subjects
# =========================================================
subjects_dir = os.path.join(ROOT, "subjects")

subjects = [
    name for name in os.listdir(subjects_dir)
    if os.path.isdir(os.path.join(subjects_dir, name))
]

subjects_sorted = sorted(subjects)


# =========================================================
# Determine CURRENT SUBJECT
# Priority: URL > session_state > fallback
# =========================================================
if url_subject:
    current_subject = url_subject
else:
    current_subject = st.session_state.get("sb_subject", subjects_sorted[0])

# Final validation
if current_subject not in subjects_sorted:
    current_subject = subjects_sorted[0]

st.session_state["sb_subject"] = current_subject


# =========================================================
# UI: SUBJECT DROPDOWN
# =========================================================
current_subject = st.selectbox(
    "Select subject:",
    subjects_sorted,
    index=subjects_sorted.index(current_subject)
)

# Update session + URL
st.session_state["sb_subject"] = current_subject
st.query_params["subject"] = current_subject


# =========================================================
# Load nodes for selected subject
# =========================================================
nodes = load_subject_nodes(current_subject)
node_names = sorted(nodes.keys())

if not node_names:
    st.error(f"No nodes found under subject `{current_subject}`")
    st.stop()


# =========================================================
# Determine CURRENT NODE
# Priority: URL > session_state > fallback
# =========================================================
if url_node:
    current_node = url_node
else:
    current_node = st.session_state.get("sb_node", node_names[0])

# Validate
if current_node not in node_names:
    current_node = node_names[0]

st.session_state["sb_node"] = current_node


# =========================================================
# UI: NODE DROPDOWN
# =========================================================
current_node = st.selectbox(
    "Select node:",
    node_names,
    index=node_names.index(current_node)
)

st.session_state["sb_node"] = current_node

# Update URL in the browser
st.query_params["subject"] = current_subject
st.query_params["node"] = current_node


# =========================================================
# Render Markdown Content
# =========================================================
markdown_path = nodes[current_node]
content = read_markdown(markdown_path)

st.markdown(content, unsafe_allow_html=True)
