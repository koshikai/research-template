import argparse
import os
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Rename the project from 'ai_research_template' to a new name."
    )
    parser.add_argument("new_name", help="New project name (snake_case)")
    args = parser.parse_args()

    new_name = args.new_name
    old_name = "ai_research_template"

    # Validation
    if not new_name.isidentifier():
        print(f"Error: '{new_name}' is not a valid Python identifier.")
        sys.exit(1)

    root_dir = Path(__file__).resolve().parent.parent

    print(f"Renaming project from '{old_name}' to '{new_name}'...")

    # 1. Rename src directory
    src_dir = root_dir / "src"
    old_package_dir = src_dir / old_name
    new_package_dir = src_dir / new_name

    if old_package_dir.exists():
        if new_package_dir.exists():
            print(
                f"Warning: Target directory {new_package_dir} already exists. "
                "Skipping directory rename."
            )
        else:
            print(f"Renaming directory: {old_package_dir} -> {new_package_dir}")
            old_package_dir.rename(new_package_dir)
    else:
        print(
            f"Warning: Source directory {old_package_dir} not found. "
            "Maybe already renamed?"
        )

    # 2. Replace string in files
    # Extensions to check
    extensions = {".py", ".toml", ".md", ".yaml", ".yml", ".json"}
    # Directories to exclude
    exclude_dirs = {
        ".git",
        ".venv",
        ".ruff_cache",
        ".pytest_cache",
        ".agent",
        "outputs",
        "data",
    }

    for root, dirs, files in os.walk(root_dir):
        # Filter directories inplace
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            file_path = Path(root) / file

            # Skip this script itself
            if file_path.name == "rename_project.py":
                continue

            if file_path.suffix in extensions or file_path.name == "uv.lock":
                try:
                    content = file_path.read_text(encoding="utf-8")
                    if old_name in content:
                        print(f"Updating content: {file_path}")
                        new_content = content.replace(old_name, new_name)

                        # Special handling for pyproject.toml name
                        if file_path.name == "pyproject.toml":
                            new_content = new_content.replace(
                                f'name = "{old_name}"', f'name = "{new_name}"'
                            )

                        file_path.write_text(new_content, encoding="utf-8")
                except Exception as e:
                    print(f"Skipping {file_path} due to error: {e}")

    print(
        "\nDone! Please run 'uv sync' to update dependencies with the new project name."
    )
    print("Recommended: Update README.md manually to reflect new project description.")


if __name__ == "__main__":
    main()
