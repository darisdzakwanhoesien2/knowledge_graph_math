# # utils/file_reader.py
# import re

# LATEX_ENVS = {
#     "bmatrix", "pmatrix", "vmatrix", "Vmatrix",
#     "matrix", "array", "align", "align*", "cases"
# }

# _env_begin_re = re.compile(r"\\begin\{([a-zA-Z*]+)\}")
# _env_end_re = re.compile(r"\\end\{([a-zA-Z*]+)\}")

# def contains_begin_env(line):
#     m = _env_begin_re.search(line)
#     return bool(m and m.group(1) in LATEX_ENVS)

# def contains_end_env(line):
#     m = _env_end_re.search(line)
#     return bool(m and m.group(1) in LATEX_ENVS)

# def repair_matrix_row(line: str) -> str:
#     """
#     FIX: Make matrix rows valid for MathJax inside Streamlit.
#     Streamlit collapses backslashes, so detect ANY number 
#     of trailing '\' and rewrite them to 4 actual backslashes.
#     """
#     s = line.rstrip()

#     # only rows with & are matrix rows
#     if "&" not in s:
#         return line

#     # detect ANY number of trailing backslashes (at least one)
#     if re.search(r"\\+$", s):
#         s = re.sub(r"\\+$", r"\\\\\\\\", s)
#         return s

#     return line



# def wrap_latex_environments(text: str) -> str:
#     lines = text.splitlines()
#     out = []

#     inside = False
#     buffer = []

#     for line in lines:
#         if not inside and contains_begin_env(line):
#             inside = True
#             buffer = [line]
#             if contains_end_env(line):
#                 inside = False
#                 out.append("$$\n" + "\n".join(buffer) + "\n$$")
#                 buffer = []
#             continue

#         if inside:
#             buffer.append(line)
#             if contains_end_env(line):
#                 inside = False
#                 out.append("$$\n" + "\n".join(buffer) + "\n$$")
#                 buffer = []
#             continue

#         out.append(line)

#     if buffer:
#         out.append("$$\n" + "\n".join(buffer) + "\n$$")

#     return "\n".join(out)


# def is_pure_latex_line(line):
#     s = line.strip()
#     if not s:
#         return False
#     if s.startswith(("#", "-", "*", ">", "`", "**", "---")):
#         return False
#     if re.search(r"[A-Za-z]{3,}", s):
#         return False
#     if re.search(r"(\\[a-zA-Z]+|[_^=+\-*/()0-9{}&])", s):
#         return True
#     return False


# def clean_latex(text: str) -> str:
#     # 1) \(..\), \[..\]
#     text = re.sub(r"\\\[(.*?)\\\]", r"$$\1$$", text, flags=re.DOTALL)
#     text = re.sub(r"\\\((.*?)\\\)", r"$\1$", text, flags=re.DOTALL)

#     # 2) Environments
#     text = wrap_latex_environments(text)

#     # 3) Process line-by-line
#     final = []
#     for line in text.splitlines():
#         # Fix matrix row endings BEFORE wrapping
#         line = repair_matrix_row(line)

#         if "$$" in line:
#             final.append(line)
#             continue

#         if is_pure_latex_line(line):
#             final.append("$$\n" + line + "\n$$")
#         else:
#             final.append(line)

#     return "\n".join(final)


# def read_markdown(path: str) -> str:
#     with open(path, "r", encoding="utf-8") as f:
#         return clean_latex(f.read())

import re

# ---------------------------------------------------------
# Normalize matrix row endings inside LaTeX blocks
# ---------------------------------------------------------
def fix_matrix_rows(latex: str) -> str:
    lines = latex.split("\n")
    out = []
    inside_math = False

    for line in lines:
        stripped = line.strip()

        # detect math block entry/exit
        if stripped.startswith("$$"):
            inside_math = not inside_math
            out.append(line)
            continue

        if inside_math:
            # ANY trailing backslashes like \, \\, \\\ → normalize to \\\\
            line = re.sub(r"\\+$", r"\\\\\\\\", line)

            # Fix cases like `\\ ` with spaces
            line = re.sub(r"\\+\s*$", r"\\\\\\\\", line)

        out.append(line)

    return "\n".join(out)

# ---------------------------------------------------------
# Convert escaped LaTeX environments
# ---------------------------------------------------------
def clean_latex(text: str) -> str:
    # Convert \[...\] to $$...$$
    text = re.sub(r"\\\[(.*?)\\\]", r"$$\1$$", text, flags=re.DOTALL)

    # Convert \(...\) to $...$
    text = re.sub(r"\\\((.*?)\\\)", r"$\1$", text, flags=re.DOTALL)

    # Remove double escaping like \\
    text = text.replace("\\\\", "\\")

    # Fix matrix row endings INSIDE $$...$$
    text = fix_matrix_rows(text)

    return text

# ---------------------------------------------------------
# Read and clean markdown file
# ---------------------------------------------------------
def read_markdown(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return clean_latex(text)
