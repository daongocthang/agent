from pathlib import Path
from .parser import parse_recipe


class Registry:
    def __init__(self, directory):
        self.directory = Path(directory)

    def list(self):
        return sorted(path.stem for path in self.directory.glob("*.md"))

    def get(self, name):
        path = self.directory / f"{name}.md"

        if not path.is_file():
            raise FileNotFoundError(f"Recipe not found: {name}")

        return parse_recipe(path)
