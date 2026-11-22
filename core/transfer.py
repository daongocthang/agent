from pathlib import Path
import re
import shlex
import subprocess

from .paths import rootpath

from .executor import build_ssh_command, validate_host

SSH_OPTIONS = [
    "-o",
    "BatchMode=yes",
    "-o",
    "ConnectTimeout=10",
]

LOCAL_DIRS = ("scripts", "snippets")


def validate_tmpfile(path):
    return re.fullmatch(r"/tmp/agent-[a-zA-Z0-9]{8}", path)


def detect_files(recipe):
    files = set()
    for step in recipe.steps:
        commands = (step.precheck, step.command, step.verify, step.rollback)

        for cmd in commands:
            if not cmd:
                continue

            for arg in shlex.split(cmd):
                path = Path(arg)

                if path.is_absolute() or ".." in path.parts:
                    continue

                if len(path.parts) < 2:
                    continue

                if path.parts[0] not in LOCAL_DIRS:
                    continue

                src = rootpath() / path
                if not src.is_file() or src.is_symlink():
                    raise ValueError(f"Invalid local file: {path}")

                files.add(path)

    return sorted(files)


def run_tool(args, timeout=60):
    result = subprocess.run(
        args,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip() or result.stdout.strip() or "Transfer failed"
        )

    return result.stdout.strip()


def create_workspace(host):
    validate_host(host)

    path = run_tool(
        ["ssh", *SSH_OPTIONS, "-T", "--", host, "mktemp -d /tmp/agent-XXXXXXXX"]
    )

    if not validate_tmpfile(path):
        raise RuntimeError("Failed to create workspace")

    return path


def upload(host, workspace, files):
    validate_host(host)

    if not validate_tmpfile(workspace):
        raise ValueError("Unsafe workspace path")

    for path in files:
        src = rootpath() / path

        if not src.is_file() or src.is_symlink():
            raise ValueError(f"Invalid local file: {path}")

        dst = f"{workspace}/{path.parent.as_posix()}"

        run_tool(build_ssh_command(host, ["mkdir", "-p", "--", dst]))

        run_tool(["scp", *SSH_OPTIONS, "-r", "--", str(src), f"{host}:{dst}/"])


def cleanup(host, workspace):
    validate_host(host)

    if not validate_tmpfile(workspace):
        raise ValueError("Unsafe workspace path")

    run_tool(build_ssh_command(host, ["rm", "-rf", "--", workspace]))
