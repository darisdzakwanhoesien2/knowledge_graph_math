import os
import json

# Define the base directory for subjects
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../subjects'))

def list_subjects():
    # Check if the BASE directory exists
    if not os.path.exists(BASE):
        raise FileNotFoundError(f"The subjects directory does not exist: {BASE}")

    # List directories inside the BASE directory
    return [d for d in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, d))]


def load_subject_nodes(subject):
    folder = os.path.join(BASE, subject, "nodes")
    return {f[:-3]: os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".md")}


def load_subject_derivations(subject):
    folder = os.path.join(BASE, subject, "derivations")
    return {f[:-3]: os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".md")}


def load_subject_narratives(subject):
    folder = os.path.join(BASE, subject, "narrative")
    return {f[:-3]: os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".md")}


def load_all_nodes(search=""):
    results = []
    for subject in list_subjects():
        nodes = load_subject_nodes(subject)
        for name, path in nodes.items():
            if search.lower() in name.lower():
                results.append((subject, name, path))
    return results


def load_relationships(subject):
    # Construct the file path dynamically
    relationships_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../subjects', subject, 'relationships'))
    file = os.path.join(relationships_dir, 'matrix_edges.json')  # Correct file name

    # Check if the file exists
    if not os.path.exists(file):
        raise FileNotFoundError(f"File not found: {file}")

    # Load the relationships from the file
    with open(file, "r") as f:
        edges = json.load(f)

    return edges