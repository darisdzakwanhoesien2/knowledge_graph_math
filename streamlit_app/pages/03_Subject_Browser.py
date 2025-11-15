import streamlit as st
from utils.loaders import list_subjects, load_subject_nodes
from utils.file_reader import read_markdown
import os

st.title("📘 Subject Browser")

# Auto-detect available subjects
subjects = list_subjects()

if not subjects:
    st.error("No subjects found in /subjects directory.")
    st.stop()

subject = st.selectbox("Select subject:", subjects)

# Try loading nodes
try:
    nodes = load_subject_nodes(subject)
except FileNotFoundError:
    st.error(f"Subject '{subject}' does not contain a nodes/ directory.")
    st.stop()

if not nodes:
    st.warning(f"No nodes found in subject '{subject}'.")
    st.stop()

selected_node = st.selectbox("Select node:", list(nodes.keys()))

st.markdown(read_markdown(nodes[selected_node]))
