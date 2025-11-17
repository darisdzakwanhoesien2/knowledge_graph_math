import os
import json

# Base directory for all subjects
BASE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../subjects")
)

# =========================================================
# SUBJECT LIST
# =========================================================
def list_subjects():
    if not os.path.exists(BASE):
        raise FileNotFoundError(f"Subjects directory not found: {BASE}")

    return [
        d for d in os.listdir(BASE)
        if os.path.isdir(os.path.join(BASE, d))
    ]


# =========================================================
# LOADERS FOR SUBJECT COMPONENTS
# =========================================================
def load_subject_nodes(subject):
    folder = os.path.join(BASE, subject, "nodes")
    if not os.path.isdir(folder):
        return {}

    return {
        f[:-3]: os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".md")
    }


def load_subject_derivations(subject):
    folder = os.path.join(BASE, subject, "derivations")
    if not os.path.isdir(folder):
        return {}

    return {
        f[:-3]: os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".md")
    }


def load_subject_narratives(subject):
    folder = os.path.join(BASE, subject, "narrative")
    if not os.path.isdir(folder):
        return {}

    return {
        f[:-3]: os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".md")
    }


# =========================================================
# GLOBAL NODE SEARCH
# =========================================================
def load_all_nodes(search=""):
    results = []
    for subject in list_subjects():
        nodes = load_subject_nodes(subject)
        for name, path in nodes.items():
            if search.lower() in name.lower():
                results.append((subject, name, path))

    return results


# =========================================================
# RELATIONSHIPS LOADER (subject-level KG)
# =========================================================
def load_relationships(subject):
    relationships_dir = os.path.join(BASE, subject, "relationships")
    json_path = os.path.join(relationships_dir, "matrix_edges.json")

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Relationship file not found: {json_path}")

    with open(json_path, "r") as f:
        return json.load(f)


# =========================================================
# Utility: find subject folder for given node name
# =========================================================
def get_node_subject(node_name):
    for subject in list_subjects():
        node_dir = os.path.join(BASE, subject, "nodes")
        if not os.path.isdir(node_dir):
            continue

        for f in os.listdir(node_dir):
            if f.endswith(".md") and f[:-3] == node_name:
                return subject

    return None
