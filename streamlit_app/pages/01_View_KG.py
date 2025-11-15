import streamlit as st
from utils.graph_builder import build_subject_graph, build_global_graph
from streamlit.components.v1 import html
import os

st.set_page_config(layout="wide")
st.title("🕸️ Knowledge Graph Viewer")

# Determine graph mode
mode = st.radio("Select Graph:", ["Subject Graph", "Global Graph"])

# Read selected node from query parameter
selected_node = st.query_params.get("selected_node", None)


# ======================================================================
# SIDEBAR: Node selected → show button to open Markdown page
# ======================================================================
with st.sidebar:
    st.header("📌 Node Selection")

    if selected_node:
        st.success(f"**Selected Node:** {selected_node}")

        if st.button("📖 Open Markdown Page"):
            # Redirect user to Subject Browser
            st.query_params["node"] = selected_node
            st.switch_page("pages/03_Subject_Browser.py")

    else:
        st.info("Click a node in the graph to select it.")


# ======================================================================
# SUBJECT GRAPH MODE
# ======================================================================
if mode == "Subject Graph":

    subjects_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../subjects")
    )

    subjects = [d for d in os.listdir(subjects_dir)
                if os.path.isdir(os.path.join(subjects_dir, d))]

    subject = st.selectbox("Select subject:", subjects)

    html_path = build_subject_graph(subject)

    st.info("Click any node to select it. Use the sidebar to open its Markdown page.")

    with open(html_path, "r", encoding="utf-8") as f:
        html_str = f.read()

    html(html_str, height=800, scrolling=True)


# ======================================================================
# GLOBAL GRAPH MODE
# ======================================================================
else:
    html_path = build_global_graph()

    st.info("Global KG: Click any node to select it. Use the sidebar to open the Markdown page.")

    with open(html_path, "r", encoding="utf-8") as f:
        html_str = f.read()

    html(html_str, height=850, scrolling=True)
