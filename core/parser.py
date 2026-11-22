import re
from pathlib import Path

from .models import Recipe, Step


def parse_recipe(path):
    content = Path(path).read_text(encoding="utf-8")

    title = re.search(
        r"^# (.+)$",
        content,
        re.MULTILINE,
    )

    if not title:
        raise ValueError("Missing doctor title")

    recipe = Recipe(name=title.group(1).strip())

    note = re.search(
        r"^## Note\s*\n(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL
    )

    if note:
        recipe.note = note.group(1).strip()
        content = content[: note.start()] + content[note.end() :]

    sections = re.split(
        r"^## Step: (.+)$",
        content,
        flags=re.MULTILINE,
    )

    for i in range(1, len(sections), 2):
        name = sections[i].strip()
        body = sections[i + 1].strip()
        blocks = {}
        commands = re.findall(
            r"^```(precheck|exec|verify|rollback)[ \t]*\n(.*?)^```[ \t]*",
            body,
            re.MULTILINE | re.DOTALL,
        )

        for kind, value in commands:
            if kind in blocks:
                raise ValueError(f"Duplicate command kind: {kind}")

            blocks[kind] = value.strip()
        if not blocks.get("exec"):
            raise ValueError(f"Missing exec:{name}")

        recipe.steps.append(
            Step(
                name=name,
                command=blocks["exec"],
                precheck=blocks.get("precheck", ""),
                verify=blocks.get("verify", ""),
                rollback=blocks.get("rollback", ""),
            )
        )

    if not recipe.steps:
        raise ValueError("No steps found")

    return recipe
