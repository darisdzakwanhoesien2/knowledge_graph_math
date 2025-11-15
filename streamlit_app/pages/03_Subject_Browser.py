import streamlit as st
from utils.loaders import list_subjects, load_subject_nodes
from utils.file_reader import read_markdown

st.title("📘 Subject Browser")

# Detect query parameters from KG Viewer
params = st.query_params

query_subject = params.get("subject", None)
query_node = params.get("node", None)

subjects = list_subjects()

# Select subject (defaults to graph-click)
subject = st.selectbox("Select subject:", subjects, index=subjects.index(query_subject) if query_subject in subjects else 0)

nodes = load_subject_nodes(subject)
node_names = list(nodes.keys())

# Node dropdown (defaults to graph-click)
if query_node in node_names:
    node_idx = node_names.index(query_node)
else:
    node_idx = 0

selected_node = st.selectbox("Select node:", node_names, index=node_idx)

# Render Markdown
st.markdown(read_markdown(nodes[selected_node]), unsafe_allow_html=True)
