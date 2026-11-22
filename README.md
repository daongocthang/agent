# Agent

Lightweight Python CLI for recipe-based Linux automation and SSH remote execution.

## Usage

```bash
agent list
agent <recipe>                        # Preview
agent <recipe> --run                  # Local
agent <recipe> --host user@host --run # Remote
agent guide remote                    # SSH guide
```

## Workflow

Load → Validate → Preview → Confirm → Transfer → Execute → Verify → Report

*Automatic transfer for remote tasks. Rollback on failure when defined.*