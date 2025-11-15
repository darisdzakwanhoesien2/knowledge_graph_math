import streamlit as st
from utils.graph_builder import build_subject_graph, build_global_graph
from streamlit.components.v1 import html
import os

st.title("🕸️ Knowledge Graph Viewer")

mode = st.radio("Select Graph:", ["Subject Graph", "Global Graph"])

if mode == "Subject Graph":
    # Define the subjects directory
    subjects_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../subjects'))

    # Check if the directory exists
    if os.path.exists(subjects_dir) and os.path.isdir(subjects_dir):
        # List directories inside the subjects directory
        subjects = [d for d in os.listdir(subjects_dir) if os.path.isdir(os.path.join(subjects_dir, d))]
    else:
        # Handle the case where the directory does not exist
        subjects = []
        print(f"Warning: The directory '{subjects_dir}' does not exist.")

    subject = st.selectbox("Select subject:", subjects)

    html_path = build_subject_graph(subject)

    with open(html_path, "r", encoding="utf-8") as f:
        html_str = f.read()

    html(html_str, height=800, scrolling=True)

else:
    html_path = build_global_graph()

    with open(html_path, "r", encoding="utf-8") as f:
        html_str = f.read()

    html(html_str, height=800, scrolling=True)