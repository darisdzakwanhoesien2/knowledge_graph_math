import streamlit as st
from utils.loaders import list_subjects, load_subject_narratives
from utils.file_reader import read_markdown

st.title("📖 Narrative Reader")

# Dynamically load subjects
subjects = list_subjects()

if not subjects:
    st.error("No subjects found in /subjects.")
    st.stop()

subject = st.selectbox("Select subject:", subjects)

# Load narratives safely
try:
    chapters = load_subject_narratives(subject)
except FileNotFoundError:
    st.error(f"Subject '{subject}' does not contain a narrative/ directory.")
    st.stop()

if not chapters:
    st.warning(f"No narrative chapters found for '{subject}'.")
    st.stop()

selected = st.selectbox("Select chapter:", list(chapters.keys()))

st.markdown(read_markdown(chapters[selected]))
