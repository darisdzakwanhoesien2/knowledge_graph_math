import streamlit as st
from utils.loaders import list_subjects, load_subject_derivations
from utils.file_reader import read_markdown
import os

st.title("🧮 Derivation Explorer")

# Auto-detect subjects
subjects = list_subjects()

if not subjects:
    st.error("No subjects found in /subjects directory.")
    st.stop()

subject = st.selectbox("Select subject:", subjects)

# Load derivations safely
try:
    derivs = load_subject_derivations(subject)
except FileNotFoundError:
    st.error(f"Subject '{subject}' does not contain a derivations/ directory.")
    st.stop()

if not derivs:
    st.warning(f"No derivations found for subject '{subject}'.")
    st.stop()

selected = st.selectbox("Select derivation:", list(derivs.keys()))

st.markdown(read_markdown(derivs[selected]))
