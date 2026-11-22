import argparse
import os
from pathlib import Path
import subprocess

from .transfer import cleanup, create_workspace, detect_files, upload

from .executor import execute
from .registry import Registry
from .reporter import report
from .paths import rootpath


def preview(recipe, host=None):
    print(f"\n Recipe: {recipe.name}")
    print(f" Target: {host or 'localhost'}")

    for i, step in enumerate(recipe.steps, 1):
        print(f"\n Step {i}: {step.name}")

        if step.precheck:
            print(f"   Precheck: {step.precheck}")

        print(f"   Execute: {step.command}")

        if step.verify:
            print(f"   Verify: {step.verify}")

        if step.rollback:
            print(f"   Rollback: {step.rollback}")


def run(recipe, timeout, host=None, workspace=None):
    executed = []

    for step in recipe.steps:
        print(f"\n[{step.name}]")

        if step.precheck:
            result = execute(step.precheck, timeout, host, workspace)
            if not report(step, "Precheck", result):
                return fail(executed, timeout, host, workspace)

        executed.append(step)
        result = execute(step.command, timeout, host, workspace)

        if not report(step, "Execute", result):
            return fail(executed, timeout, host, workspace)

        if step.verify:
            result = execute(step.verify, timeout, host, workspace)
            if not report(step, "Verify", result):
                return fail(executed, timeout, host, workspace)

    return True


def fail(executed, timeout, host, workspace):
    print("\n✘ Execution stopped")

    if not executed:
        print("No steps executed")
        return False

    complete = rollback(executed, timeout, host, workspace)

    if complete:
        print("\n✔ All declared rollbacks succeeded")
    else:
        print("\n✘ Rollback incomplete. Manual review required.")

    return False


def rollback(steps, timeout, host, workspace):
    print("\nRollback started...")
    complete = True
    for step in reversed(steps):
        if not step.rollback:
            print(f"  ⊘ Rollback: {step.name} (not defined)")
            complete = False
            continue

        result = execute(step.rollback, timeout, host, workspace)

        if not report(step, "Rollback", result):
            complete = False

    return complete


def main():
    parser = argparse.ArgumentParser(prog="agent")
    parser.add_argument("name", nargs="?", help="Recipe name or 'list'")
    parser.add_argument("topic", nargs="?", help="Guide topic")
    parser.add_argument(
        "--host",
        metavar="USER@HOST",
        help="SSH host (default: localhost)",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Execute after confirmation",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        metavar="SECONDS",
        help="Timeout for each command (default: 30)",
    )

    args = parser.parse_args()
    if args.name == "guide":
        from .guide import show_guide

        try:
            show_guide(args.topic)
        except ValueError as er:
            parser.error(str(er))

        return

    if args.timeout <= 0:
        parser.error("--timeout must be positive")

    directory = Path(
        os.environ.get("AGENT_RECIPES", rootpath() / "recipes")
    ).expanduser()
    registry = Registry(directory)

    if not args.name or args.name == "list":
        for name in registry.list():
            print(name)
        return

    try:
        recipe = registry.get(args.name)
    except (FileNotFoundError, ValueError) as er:
        parser.error(str(er))

    preview(recipe, args.host)

    if not args.run:
        print("\nDry-run only. Use --run to execute")
        return

    if input("\nContinue? [y/N]: ").strip().lower() != "y":
        print("Cancelled")
        return

    workspace = None
    cleanup_ok = True
    success = False
    try:
        files = detect_files(recipe) if args.host else []

        if args.host and files:
            workspace = create_workspace(args.host)

            print(f"\nWorkspace: {workspace}")
            print(f"Transferring {len(files)} file(s)...")

            upload(args.host, workspace, files)
            print("✔ Transfer completed")

        success = run(recipe, args.timeout, args.host, workspace)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as er:
        print(f"\n✘ Agent error: {er}")
    finally:
        if workspace:
            try:
                cleanup(args.host, workspace)
                print("\n✔ Workspace cleaned up")
            except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as er:
                print(f"\n✘ Cleanup failed: {er}")
                print(f"Manual cleanup required: {workspace}")

    if success and cleanup_ok:
        print("\n✔ Recipe completed")

        if recipe.note:
            print(f"\nNote:\n{recipe.note}")

    else:
        print("\n✘ Recipe failed")
        raise SystemExit(1)
