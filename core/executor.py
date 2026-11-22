import re
import shlex
import subprocess

from .models import Result


def validate_host(host):
    if not re.fullmatch(r"(?:[a-zA-Z0-9_.-]+@)?[a-zA-Z0-9_.-]+", host):
        raise ValueError("Invalid SSH host")


def build_ssh_command(host, args, workspace=None):
    validate_host(host)

    command = shlex.join(args)
    if workspace:
        command = f"cd {shlex.quote(workspace)} && {command}"

    return [
        "ssh",
        "-T",
        "-o",
        "BatchMode=yes",
        "-o",
        "ConnectTimeout=10",
        "--",
        host,
        command,
    ]


def execute(command, timeout=30, host=None, workspace=None):
    try:

        args = shlex.split(command)

        if not args:
            raise ValueError("Command cannot be empty")

        if host:
            args = build_ssh_command(host, args, workspace)

        result = subprocess.run(
            args,
            shell=False,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
        )

        output = "\n".join(
            part.strip() for part in (result.stdout, result.stderr) if part.strip()
        )

        return Result(result.returncode, output)

    except subprocess.TimeoutExpired:
        return Result(124, "Command timed out")

    except (ValueError, OSError) as er:
        return Result(1, str(er))
