import sys
import os

# =========================================================
# Fix Python paths
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
# Sync URL param → session_state
# =========================================================
params = st.query_params

if "selected_node" in params:
    url_node = params["selected_node"]
    if st.session_state.get("selected_node") != url_node:
        st.session_state["selected_node"] = url_node
        st.rerun()


# =========================================================
# Page Config
# =========================================================
st.set_page_config(layout="wide")
st.title("🕸️ Knowledge Graph Viewer")


# =========================================================
# Helper: detect subject for node
# =========================================================
def detect_subject_for_node(node_name: str):
    subjects_dir = os.path.join(ROOT, "subjects")

    for subject in os.listdir(subjects_dir):
        node_path = os.path.join(subjects_dir, subject, "nodes", f"{node_name}.md")
        if os.path.exists(node_path):
            return subject

    return None


# =========================================================
# Sidebar — Search Dropdown then Node Info
# =========================================================
with st.sidebar:

    # ---------------------------------------------------
    # SEARCH DROPDOWN (TOP)
    # ---------------------------------------------------
    st.header("🔍 Search Node")

    subjects_dir = os.path.join(ROOT, "subjects")
    all_nodes = []
    subject_map = {}

    for subject in os.listdir(subjects_dir):
        node_dir = os.path.join(subjects_dir, subject, "nodes")
        if not os.path.isdir(node_dir):
            continue

        for f in os.listdir(node_dir):
            if f.endswith(".md"):
                node_name = f[:-3]
                all_nodes.append(node_name)
                subject_map[node_name] = subject

    all_nodes_sorted = sorted(set(all_nodes))

    prev_dropdown_value = st.session_state.get("search_dropdown_value", "")

    picked = st.selectbox("Select Node:", [""] + all_nodes_sorted)

    st.session_state["search_dropdown_value"] = picked

    # If user selects a NEW node → update selected_node + rerun
    if picked != "" and picked != prev_dropdown_value:
        st.session_state["selected_node"] = picked
        st.session_state["selected_subject"] = subject_map.get(picked)
        st.rerun()

    st.divider()

    # ---------------------------------------------------
    # NODE SELECTION (from graph or dropdown)
    # ---------------------------------------------------
    st.header("📌 Node Selection")

    selected_node = st.session_state.get("selected_node", None)
    selected_subject = st.session_state.get("selected_subject", None)

    if selected_node:

        # Auto-detect subject if not stored yet
        if selected_subject is None:
            detected = detect_subject_for_node(selected_node)
            st.session_state["selected_subject"] = detected
            selected_subject = detected

        st.success(f"Selected Node: **{selected_node}**")

        if selected_subject:
            st.caption(f"Subject: `{selected_subject}`")
        else:
            st.caption("Subject: *(unknown)*")

        if st.button("📖 Open Markdown Page"):
            if selected_subject:
                st.query_params["subject"] = selected_subject
                st.query_params["node"] = selected_node
                st.switch_page("pages/03_Subject_Browser.py")
            else:
                st.error("Subject cannot be detected for this node.")
    else:
        st.info("Click a node OR select via dropdown.")


# =========================================================
# Main Graph Section
# =========================================================
mode = st.radio("Select Graph:", ["Subject Graph", "Global Graph"])

if mode == "Subject Graph":

    subjects_dir = os.path.join(ROOT, "subjects")
    subjects = [
        d for d in os.listdir(subjects_dir)
        if os.path.isdir(os.path.join(subjects_dir, d))
    ]

    # Default subject = numerical_matrix_analysis
    default_index = subjects.index("numerical_matrix_analysis") if "numerical_matrix_analysis" in subjects else 0

    subject = st.selectbox("Select subject:", subjects, index=default_index)

    html_path = build_subject_graph(subject)

    st.info("Click a blue node in the graph → Sidebar updates instantly.")

    with open(html_path, "r", encoding="utf-8") as f:
        html_str = f.read()

    html(html_str, height=800, scrolling=True)

else:
    html_path = build_global_graph()

    st.info("Global graph: click any existing node to load it.")

    with open(html_path, "r", encoding="utf-8") as f:
        html_str = f.read()

    html(html_str, height=850, scrolling=True)

