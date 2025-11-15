import streamlit as st
from utils.graph_builder import build_subject_graph, build_global_graph
from streamlit.components.v1 import html
import os

st.set_page_config(layout="wide")
st.title("🕸️ Knowledge Graph Viewer")


# =============================
# Graph Mode Selection
# =============================
mode = st.radio("Select Graph:", ["Subject Graph", "Global Graph"])


# =============================
# SUBJECT GRAPH MODE
# =============================
if mode == "Subject Graph":

    # Detect subjects directory
    subjects_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../subjects")
    )

    if not os.path.exists(subjects_dir):
        st.error(f"❌ Subjects directory not found:\n{subjects_dir}")
        st.stop()

    subjects = [
        d for d in os.listdir(subjects_dir)
        if os.path.isdir(os.path.join(subjects_dir, d))
    ]

    if not subjects:
        st.warning("⚠️ No subjects found in /subjects directory.")
        st.stop()

    # Subject dropdown
    subject = st.selectbox("Select subject:", subjects)

    # Build graph for the selected subject
    html_path = build_subject_graph(subject)

    st.info(
        "💡 **Tip:** Click any blue node in the graph to open its Markdown page.\n"
        "This automatically navigates to:\n"
        "➡️ **Subject Browser → (subject) → (node)**"
    )

    # Render graph HTML
    with open(html_path, "r", encoding="utf-8") as f:
        html_str = f.read()

    # Display inside iframe (no sandbox options required)
    html(html_str, height=800, scrolling=True)


# =============================
# GLOBAL GRAPH MODE
# =============================
else:

    # Build global graph file
    html_path = build_global_graph()

    st.info(
        "🌍 **Global Knowledge Graph:** merged view of all subjects.\n"
        "Clicking a node opens its Markdown page (if subject is known)."
    )

    with open(html_path, "r", encoding="utf-8") as f:
        html_str = f.read()

    html(html_str, height=850, scrolling=True)
