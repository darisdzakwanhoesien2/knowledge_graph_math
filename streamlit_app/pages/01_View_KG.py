import streamlit as st
import os
from utils.graph_builder import build_subject_graph, build_global_graph
from streamlit.components.v1 import html

st.set_page_config(layout="wide")
st.title("🕸️ Knowledge Graph Viewer")

# Select graph mode
mode = st.radio("Select Graph:", ["Subject Graph", "Global Graph"])


# -------------------------------------------------------------------------
# SUBJECT GRAPH MODE
# -------------------------------------------------------------------------
if mode == "Subject Graph":

    # Compute absolute path to the /subjects directory
    subjects_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../subjects")
    )

    # Load subjects dynamically
    if os.path.exists(subjects_dir):
        subjects = [
            d for d in os.listdir(subjects_dir)
            if os.path.isdir(os.path.join(subjects_dir, d))
        ]
    else:
        st.error(f"Subjects directory not found: {subjects_dir}")
        st.stop()

    if not subjects:
        st.warning("No subjects found in /subjects directory.")
        st.stop()

    subject = st.selectbox("Select subject:", subjects)

    # Build the knowledge graph HTML
    html_path = build_subject_graph(subject)

    # Show instructions
    st.info(
        "💡 **Tip:** Click any node in the graph to open its Markdown page.\n\n"
        "This will automatically navigate to:\n"
        "**Subject Browser → (subject) → (node)**"
    )

    # Read graph HTML
    with open(html_path, "r", encoding="utf-8") as f:
        html_str = f.read()

    # Render
    html(html_str, height=800, scrolling=True)


# -------------------------------------------------------------------------
# GLOBAL GRAPH MODE
# -------------------------------------------------------------------------
else:
    html_path = build_global_graph()

    st.info(
        "🌍 **Global Knowledge Graph** combines all subjects.\n"
        "Clicking nodes may not navigate to Markdown pages unless cross-links are defined."
    )

    # Read and display global graph
    with open(html_path, "r", encoding="utf-8") as f:
        html_str = f.read()

    html(html_str, height=800, scrolling=True)
