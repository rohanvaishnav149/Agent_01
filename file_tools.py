"""PHASE 2: safe file tools that the AI is allowed to use.

The AI can ONLY touch files inside the workspace/ folder.
Creating or changing a file needs the student to type yes.
"""
import difflib
from pathlib import Path

from langchain_core.tools import tool


WORKSPACE = Path(__file__).resolve().parent / "workspace"
WORKSPACE.mkdir(exist_ok=True)

ALLOWED_TYPES = {".py", ".js", ".html", ".css", ".txt", ".md", ".json"}


def safe_path(filename):
    """Check the filename and return its path inside workspace/."""
    filename = filename.strip()

    if not filename or any(sign in filename for sign in ["/", "\\", ":", ".."]):
        raise ValueError("Use only a simple filename like hello.py (no folders).")

    if Path(filename).suffix.lower() not in ALLOWED_TYPES:
        raise ValueError("Allowed file types: " + ", ".join(sorted(ALLOWED_TYPES)))

    return WORKSPACE / filename


def ask_yes(title, preview):
    """Show a preview and return True only if the student types yes."""
    print("\n" + "=" * 50)
    print(title)
    print("-" * 50)
    print(preview)
    print("=" * 50)
    answer = input("Type yes to approve (anything else cancels): ")
    return answer.strip().lower() in {"yes", "y"}


@tool
def list_files() -> str:
    """List all files inside the workspace folder."""
    names = [p.name for p in sorted(WORKSPACE.iterdir())
             if p.is_file() and p.name != ".gitkeep"]
    return "\n".join(names) if names else "The workspace is empty."


@tool
def read_file(filename: str) -> str:
    """Read a file from the workspace. Use this before explaining or editing it."""
    path = safe_path(filename)
    if not path.exists():
        return f"{filename} does not exist in the workspace."
    return path.read_text(encoding="utf-8")


@tool
def create_file(filename: str, content: str) -> str:
    """Create a NEW file in the workspace. The student must approve it first."""
    path = safe_path(filename)
    if path.exists():
        return f"{filename} already exists. Ask to edit it instead."

    if not ask_yes(f"CREATE FILE: {filename}", content):
        return "The student cancelled. No file was created."

    path.write_text(content, encoding="utf-8")
    return f"Created {filename}."


@tool
def edit_file(filename: str, new_content: str) -> str:
    """Replace an existing workspace file with new_content (the COMPLETE new file).
    The student sees the changes and must approve them first."""
    path = safe_path(filename)
    if not path.exists():
        return f"{filename} does not exist. Create it first."

    old_content = path.read_text(encoding="utf-8")
    if old_content == new_content:
        return "No changes were needed."

    changes = "\n".join(difflib.unified_diff(
        old_content.splitlines(), new_content.splitlines(),
        "old/" + filename, "new/" + filename, lineterm=""))

    if not ask_yes(f"EDIT FILE: {filename}  (- removed, + added)", changes):
        return "The student cancelled. The file was not changed."

    path.write_text(new_content, encoding="utf-8")
    return f"Updated {filename}."


# The list of tools we give to the AI. Nothing else is allowed.
ALL_TOOLS = [list_files, read_file, create_file, edit_file]


# Quick test without AI:  python file_tools.py
if __name__ == "__main__":
    print("Files:", list_files.invoke({}))
    try:
        safe_path("../secret.py")
    except ValueError as error:
        print("Blocked unsafe name:", error)
