import re

# ---------------------------------------------------------
# 1. Detect PURE LaTeX math line (strict)
# ---------------------------------------------------------
def is_pure_latex(line: str) -> bool:
    s = line.strip()

    # Ignore empty lines and markdown structure
    if (
        not s
        or s[0] in "#-*>|"
        or s.startswith("**")
        or s.startswith("---")
        or "|" in s  # tables
        or ":" in s  # labels or explanations
    ):
        return False

    # Contains English words → NOT math
    if re.search(r"[A-Za-z]{3,}", s):
        return False

    # It must contain some math-specific tokens
    if not re.search(r"(\\[a-zA-Z]+|[_^=+\-*/()0-9])", s):
        return False

    return True


# ---------------------------------------------------------
# 2. Fix LaTeX syntax safely
# ---------------------------------------------------------
def clean_latex(text: str) -> str:
    # Convert \[...\] to $$...$$
    text = re.sub(r"\\\[(.*?)\\\]", r"$$\1$$", text, flags=re.DOTALL)

    # Convert inline \(..\) to $..$
    text = re.sub(r"\\\((.*?)\\\)", r"$\1$", text, flags=re.DOTALL)

    # Remove double escaping
    text = text.replace("\\\\", "\\")

    result = []
    for line in text.split("\n"):
        stripped = line.strip()

        # Do NOT touch markdown structure
        if stripped.startswith(("#", "-", "*", ">", "|", "##", "**", "---")):
            result.append(line)
            continue

        # PURE math line → wrap with $$
        if is_pure_latex(stripped):
            if not (stripped.startswith("$") and stripped.endswith("$")):
                line = f"$$\n{stripped}\n$$"

        result.append(line)

    return "\n".join(result)


def read_markdown(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return clean_latex(text)
