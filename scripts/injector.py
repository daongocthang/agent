#!/usr/bin/env python3


import argparse
import hashlib
import os
from pathlib import Path
import sys


def managed_block(snippet):
    name = Path(snippet).stem.lower()
    content = snippet.read_text(encoding="utf-8").rstrip("\n")

    if not content:
        raise ValueError("Empty snippet")

    block_id = hashlib.sha256(name.encode("utf-8")).hexdigest()[:12]

    return f"# BEGIN AGENT: {block_id}\n" f"{content}\n" f"# END AGENT: {block_id}\n"


def read_target(target):
    if not target.exists():
        return ""

    if not target.is_file():
        raise ValueError("Target is not a regular file")

    return target.read_text(encoding="utf-8")


def write_target(target, content):
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        mode = target.stat().st_mode & 0o777
    else:
        mode = 0o600

    tmp = target.with_name(target.name + ".agent.tmp")
    try:
        with tmp.open("w", encoding="utf-8") as f:
            f.write(content)

        os.chmod(tmp, mode)
        os.rename(tmp, target)
    finally:
        if tmp.exists():
            tmp.unlink()


def add(target, block):
    content = read_target(target)

    if block in content:
        print("Already installed")
        return

    start = block.splitlines()[0]
    if start in content:
        raise ValueError("Managed block has been modified")

    sep = "" if not content or content.endswith("\n") else "\n"

    write_target(target, content + sep + block)


def check(target, block):
    content = read_target(target)

    if block not in content:
        print("Not installed")
        return False

    print("Installed")
    return True


def remove(target, block):
    content = read_target(target)
    if block not in content:
        print("Nothing to remove")
        return

    write_target(target, content.replace(block, "", 1))
    print("Removed")


def main():
    parser = argparse.ArgumentParser(prog="injector")
    parser.add_argument("action", choices=["add", "check", "remove"])
    parser.add_argument("target")
    parser.add_argument("snippet")

    args = parser.parse_args()

    target = Path(args.target).expanduser()
    snippet = Path(args.snippet).expanduser()

    try:
        block = managed_block(snippet)
        if args.action == "add":
            add(target, block)
        elif args.action == "check":
            if not check(target, block):
                raise SystemExit(1)

        elif args.action == "remove":
            remove(target, block)
    except (OSError, UnicodeError, ValueError) as er:
        print(f"Error: {er}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
