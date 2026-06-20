import re

# ---------------------------------------------------------
# Normalize matrix row endings inside $$ ... $$ blocks.
# Streamlit collapses single backslashes, so trailing `\`
# or `\\` in a matrix row must become `\\\\` (four slashes)
# so MathJax receives the literal `\\` it needs.
# ---------------------------------------------------------
def fix_matrix_rows(latex: str) -> str:
    lines = latex.split("\n")
    out = []
    inside_math = False

    for line in lines:
        stripped = line.strip()

        # Toggle math-block state on $$ delimiters
        if stripped.startswith("$$"):
            inside_math = not inside_math
            out.append(line)
            continue

        if inside_math:
            # Normalize any trailing backslash sequence to exactly \\\\
            # Handles: \, \\, \\\ , \\ <spaces>, etc.
            line = re.sub(r"\\+\s*$", r"\\\\\\\\", line)

        out.append(line)

    return "\n".join(out)


# ---------------------------------------------------------
# Convert common LaTeX delimiters to the $$ / $ form that
# Streamlit's st.markdown expects, then fix matrix rows.
# ---------------------------------------------------------
def clean_latex(text: str) -> str:
    # Convert \[...\]  →  $$...$$  (display math)
    text = re.sub(r"\\\[(.*?)\\\]", r"$$\1$$", text, flags=re.DOTALL)

    # Convert \(...\)  →  $...$    (inline math)
    text = re.sub(r"\\\((.*?)\\\)", r"$\1$", text, flags=re.DOTALL)

    # NOTE: Do NOT call text.replace("\\\\", "\\") here.
    # The previous version did this, which silently broke matrix
    # row separators (\\) inside $$ blocks before fix_matrix_rows
    # had a chance to normalise them.

    # Fix matrix row endings inside $$ blocks
    text = fix_matrix_rows(text)

    return text


# ---------------------------------------------------------
# Read a Markdown file and apply LaTeX normalisation.
# ---------------------------------------------------------
def read_markdown(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return clean_latex(text)
