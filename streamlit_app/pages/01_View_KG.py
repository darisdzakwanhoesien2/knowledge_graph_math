import sys
import os

# =========================================================
# Fix Python path to import utils/ and subjects/
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
# Page config
# =========================================================
st.set_page_config(layout="wide")
st.title("🕸️ Knowledge Graph Viewer")


# =========================================================
# --- Sync selected_node from URL query params (if present)
# =========================================================
params = st.query_params
if "selected_node" in params:
    url_node = params["selected_node"]
    # only update + rerun if changed
    if st.session_state.get("selected_node") != url_node:
        st.session_state["selected_node"] = url_node
        st.rerun()

# local var for convenience
selected_node = st.session_state.get("selected_node", None)


# =========================================================
# Helper: find subject folder which contains the node
# =========================================================
def detect_subject_for_node(node_name: str):
    subjects_dir = os.path.join(ROOT, "subjects")
    for subject in os.listdir(subjects_dir):
        node_path = os.path.join(subjects_dir, subject, "nodes", f"{node_name}.md")
        if os.path.exists(node_path):
            return subject
    return None


# =========================================================
# Sidebar
# =========================================================
with st.sidebar:
    st.header("📌 Node Selection")

    # If a node was selected (either by graph click or dropdown)
    if st.session_state.get("selected_node"):
        cur = st.session_state["selected_node"]
        st.success(f"Selected Node: **{cur}**")

        # Show which subject contains it (optional)
        detected_subj = detect_subject_for_node(cur)
        if detected_subj:
            st.caption(f"Subject: `{detected_subj}`")
        else:
            st.caption("Subject: (not found on disk)")

        # Button to actually open the markdown page (user-controlled)
        if st.button("📖 Open Markdown Page"):
            # prefer session_state subject if present (set by dropdown),
            # otherwise attempt to detect automatically
            subject_to_open = st.session_state.get("selected_subject") or detected_subj
            node_to_open = st.session_state["selected_node"]

            if subject_to_open and node_to_open:
                # set query params then switch to subject browser
                st.query_params["subject"] = subject_to_open
                st.query_params["node"] = node_to_open
                # switch_page expects the page name under pages/
                st.switch_page("pages/03_Subject_Browser.py")
            else:
                st.warning("Could not determine subject or node to open.")

    else:
        st.info("Click a node in the graph or pick one from Search.")


    st.markdown("---")
    st.header("🔍 Search Node (dropdown)")

    # collect all nodes across subjects (subject graph focus: numerical_matrix_analysis)
    subjects_dir = os.path.join(ROOT, "subjects")
    all_nodes = []
    subject_map = {}

    for subject in os.listdir(subjects_dir):
        node_dir = os.path.join(subjects_dir, subject, "nodes")
        if not os.path.isdir(node_dir):
            continue
        for f in os.listdir(node_dir):
            if f.endswith(".md"):
                nn = f[:-3]
                all_nodes.append(nn)
                subject_map[nn] = subject

    all_nodes_sorted = sorted(set(all_nodes))

    # Dropdown. When user picks, we store node+subject in session_state but DO NOT redirect.
    picked = st.selectbox("Select Node:", [""] + all_nodes_sorted, index=0)

    if picked:
        # store selection (no immediate redirect)
        st.session_state["selected_node"] = picked
        st.session_state["selected_subject"] = subject_map.get(picked)


# =========================================================
# MAIN (focus on Subject Graph)
# =========================================================
st.subheader("Subject Graph (numerical_matrix_analysis)")

# default target subject (you asked to focus on this first)
default_subject = "numerical_matrix_analysis"

# If subject folder exists use it, otherwise pick first available
subjects_dir = os.path.join(ROOT, "subjects")
if os.path.isdir(os.path.join(subjects_dir, default_subject)):
    subject = default_subject
else:
    # fallback: pick the first subject available
    candidates = [d for d in os.listdir(subjects_dir) if os.path.isdir(os.path.join(subjects_dir, d))]
    subject = candidates[0] if candidates else ""

# show subject selection (readonly / informative)
st.info(f"Rendering subject graph for **{subject}**")

# build and render the subject graph HTML (pyvis)
html_path = build_subject_graph(subject)

# Inform user on how graph selection behaves
st.info("Click any blue node in the graph → it will populate the sidebar. Use the sidebar button to open the Markdown page.")

with open(html_path, "r", encoding="utf-8") as fh:
    html_str = fh.read()

# Use the html component to embed the generated pyvis HTML
html(html_str, height=800, scrolling=True)
