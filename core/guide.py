from .paths import rootpath


def show_guide(name=None):
    directory = rootpath() / "docs"

    if name is None:
        for path in sorted(directory.glob("*.md")):
            print(path.stem)
        return

    path = directory / f"{name}.md"
    if not path.is_file():
        raise ValueError(f"Guide not found: {name}")

    print(path.read_text(encoding="utf-8"))
