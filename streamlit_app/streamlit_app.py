import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from utils.graph_builder import build_subject_graph, build_global_graph

import streamlit as st
import os
import json

st.set_page_config(
    page_title="Knowledge Graph Hub",
    layout="wide"
)

st.title("📚 Knowledge Graph Navigation Hub")

st.markdown("""
Welcome to the **Knowledge Graph Explorer**.

Choose one of the pages on the left to:
- Explore subjects
- Visualize knowledge graphs
- Browse nodes and derivations
- Read narrative chapters
- Upload PDFs to auto-extract topics
""")

# List subjects dynamically
# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Correctly define the subjects directory
subjects_dir = os.path.join(current_dir, "../subjects")

# Ensure the path exists
if not os.path.exists(subjects_dir):
    raise FileNotFoundError(f"The subjects directory does not exist: {subjects_dir}")

# List directories in the subjects folder
subjects = [d for d in os.listdir(subjects_dir) if os.path.isdir(os.path.join(subjects_dir, d))]

st.subheader("Available Subjects")
for sub in subjects:
    s_path = os.path.join(subjects_dir, sub, "index.json")
    if os.path.exists(s_path):
        with open(s_path, "r") as f:
            meta = json.load(f)
        st.markdown(f"- **{meta.get('subject', sub)}** — {meta.get('description', '')}")
    else:
        st.markdown(f"- **{sub}**")