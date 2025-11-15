import os
import streamlit.components.v1 as components

# Absolute path to frontend directory
_component_dir = os.path.dirname(__file__)
_frontend_dir = os.path.join(_component_dir, "frontend")

# Declare Streamlit component
_node_selector = components.declare_component(
    "node_selector",
    path=_frontend_dir
)

def node_selector(default=None):
    """Wrapper for our custom node selector component."""
    return _node_selector(default=default)
