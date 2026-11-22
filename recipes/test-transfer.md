
# Test Phase 5

Test automatic remote transfer, execution and verification.

## Step: Create Test File

```precheck
python3 -V
```

```exec
python3 scripts/test-transfer.py write snippets/test-transfer.txt
```

```verify
python3 scripts/test-transfer.py check snippets/test-transfer.txt
```

```rollback
python3 scripts/test-transfer.py remove
```

## Step: Check Remote Host

```exec
hostname
```

## Step: Check Working Directory

```exec
pwd
```

## Note

Test file: /tmp/agent-phase5-test.txt

After testing, remove the test file manually if rollback was not triggered.
