import streamlit as st
from utils.loaders import list_subjects, load_subject_nodes
from utils.file_reader import read_markdown

st.title("🔍 Node Browser (with Filter)")

# Select subject
subjects = list_subjects()
selected_subject = st.selectbox("Subject:", subjects)

# Load all nodes of that subject
nodes = load_subject_nodes(selected_subject)
node_names = list(nodes.keys())

# Optional search filter
search_term = st.text_input("Filter nodes:", "").lower()

if search_term:
    filtered_nodes = [n for n in node_names if search_term in n.lower()]
else:
    filtered_nodes = node_names

if not filtered_nodes:
    st.warning("No nodes match your filter.")
else:
    selected_node = st.selectbox("Select node:", filtered_nodes)
    st.markdown(read_markdown(nodes[selected_node]))
