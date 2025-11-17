import sys
import os
import streamlit as st
from streamlit.components.v1 import html
from utils.graph_builder import build_subject_graph, build_global_graph

# =========================================================
# Fix Python paths
# =========================================================
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ROOT = os.path.abspath(os.path.join(BASE, '..'))
sys.path.append(BASE)
sys.path.append(ROOT)

# =========================================================
# Page Config
# =========================================================
st.set_page_config(layout="wide")
st.title("🕸️ Knowledge Graph Viewer")

# =========================================================
# Sync URL param → session_state
# =========================================================
params = st.query_params

if "selected_node" in params:
    node_from_url = params["selected_node"]
    if st.session_state.get("selected_node") != node_from_url:
        st.session_state["selected_node"] = node_from_url
        st.session_state["selected_subject"] = None
        st.rerun()

# =========================================================
# Helper: detect subject from node name
# =========================================================
def detect_subject_for_node(node_name: str):
    subjects_path = os.path.join(ROOT, "subjects")
    for subject in os.listdir(subjects_path):
        md_path = os.path.join(subjects_path, subject, "nodes", f"{node_name}.md")
        if os.path.exists(md_path):
            return subject
    return None

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    # ----------------------------------------------------
    # SEARCH DROPDOWN
    # ----------------------------------------------------
    st.header("🔍 Search Node")

    subjects_root = os.path.join(ROOT, "subjects")
    all_nodes = []
    subject_map = {}

    for subject in os.listdir(subjects_root):
        node_dir = os.path.join(subjects_root, subject, "nodes")
        if not os.path.isdir(node_dir):
            continue
        for fname in os.listdir(node_dir):
            if fname.endswith(".md"):
                name = fname[:-3]
                all_nodes.append(name)
                subject_map[name] = subject

    all_nodes_sorted = sorted(set(all_nodes))

    previous_choice = st.session_state.get("search_dropdown_value", "")

    picked = st.selectbox("Select Node:", [""] + all_nodes_sorted)

    st.session_state["search_dropdown_value"] = picked

    # If changed → update selected node and rerun
    if picked and picked != previous_choice:
        st.session_state["selected_node"] = picked
        st.session_state["selected_subject"] = subject_map.get(picked)
        st.rerun()

    st.divider()

    # ----------------------------------------------------
    # NODE SELECTION (graph click OR dropdown)
    # ----------------------------------------------------
    st.header("📌 Node Selection")

    selected_node = st.session_state.get("selected_node", None)
    selected_subject = st.session_state.get("selected_subject", None)

    if selected_node:

        # auto detect subject if not known
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
            if not selected_subject:
                st.error("Cannot open page: subject unknown.")
                st.stop()

            # update query params BEFORE switching page
            st.query_params["subject"] = selected_subject
            st.query_params["node"] = selected_node

            # now switch (Streamlit keeps params in URL)
            st.switch_page("pages/03_Subject_Browser.py")
    else:
        st.info("Click a graph node OR select from dropdown.")

# =========================================================
# MAIN GRAPH SECTION
# =========================================================
mode = st.radio("Select Graph:", ["Subject Graph", "Global Graph"])

if mode == "Subject Graph":
    subjects_root = os.path.join(ROOT, "subjects")
    subjects = [
        d for d in os.listdir(subjects_root)
        if os.path.isdir(os.path.join(subjects_root, d))
    ]

    default = "numerical_matrix_analysis"
    idx = subjects.index(default) if default in subjects else 0

    selected_subject_for_graph = st.selectbox(
        "Select subject:", subjects, index=idx
    )

    html_path = build_subject_graph(selected_subject_for_graph)

    st.info("Click a blue node in the graph → Sidebar updates immediately.")

    with open(html_path, "r", encoding="utf-8") as f:
        graph_html = f.read()

    html(graph_html, height=800, scrolling=True)

else:
    html_path = build_global_graph()

    st.info("Global graph: click any existing node to update the sidebar.")

    with open(html_path, "r", encoding="utf-8") as f:
        graph_html = f.read()

    html(graph_html, height=850, scrolling=True)
