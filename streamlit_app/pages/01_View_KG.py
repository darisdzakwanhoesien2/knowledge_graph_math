import sys
import os

# =========================================================
# Fix Python path to import utils/ and components/
# =========================================================
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ROOT = os.path.abspath(os.path.join(BASE, '..'))

sys.path.append(BASE)    # streamlit_app/
sys.path.append(ROOT)    # project root/


# =========================================================
# Imports
# =========================================================
import streamlit as st
from streamlit.components.v1 import html

from utils.graph_builder import build_subject_graph, build_global_graph


# =========================================================
# Sync selected_node from URL query parameters
# =========================================================
params = st.query_params

if "selected_node" in params:
    url_node = params["selected_node"]

    # If it changed from previous run → update + rerun
    if st.session_state.get("selected_node") != url_node:
        st.session_state["selected_node"] = url_node
        st.rerun()


# =========================================================
# Page Setup
# =========================================================
st.set_page_config(layout="wide")
st.title("🕸️ Knowledge Graph Viewer")


# =========================================================
# Sidebar — Node Info Panel
# =========================================================
selected_node = st.session_state.get("selected_node", None)

with st.sidebar:
    st.header("📌 Node Selection")

    if selected_node:
        st.success(f"Selected Node: **{selected_node}**")

        if st.button("📖 Open Markdown Page"):
            # Route to Subject Browser with selected node
            st.query_params["node"] = selected_node
            st.switch_page("pages/03_Subject_Browser.py")
    else:
        st.info("Click a node in the graph to select it.")


# =========================================================
# Graph Mode Selection
# =========================================================
mode = st.radio("Select Graph:", ["Subject Graph", "Global Graph"])


# =========================================================
# SUBJECT GRAPH VIEW
# =========================================================
if mode == "Subject Graph":

    subjects_dir = os.path.join(ROOT, "subjects")

    subjects = [
        d for d in os.listdir(subjects_dir)
        if os.path.isdir(os.path.join(subjects_dir, d))
    ]

    subject = st.selectbox("Select subject:", subjects)

    # Build PyVis graph HTML
    html_path = build_subject_graph(subject)

    st.info("Click a node in the graph. It will appear in the sidebar.")

    with open(html_path, "r", encoding="utf-8") as f:
        html_str = f.read()

    html(html_str, height=800, scrolling=True)


# =========================================================
# GLOBAL GRAPH VIEW
# =========================================================
else:

    html_path = build_global_graph()

    st.info("Click a node in the graph. It will appear in the sidebar.")

    with open(html_path, "r", encoding="utf-8") as f:
        html_str = f.read()

    html(html_str, height=850, scrolling=True)
