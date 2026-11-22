#!/usr/bin/env python3

import sys
from pathlib import Path

action = sys.argv[1]
target = Path("/tmp/agent-phase5-test.txt")

if action == "write":
    content = Path(sys.argv[2]).read_text()
    target.write_text(content)
    print("File created:", target)

elif action == "check":
    expected = Path(sys.argv[2]).read_text()
    if not target.is_file() or target.read_text() != expected:
        sys.exit("Verification failed")
    print("Verification successful")

elif action == "remove":
    target.unlink(missing_ok=True)
    print("File removed")
