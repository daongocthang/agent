
# Test Rollback

Test declared rollback with temporary files.

## Step: Create File A

```precheck
test ! -e /tmp/agent-phase3-a.tmp
```

```exec
touch /tmp/agent-phase3-a.tmp
```

```verify
test -f /tmp/agent-phase3-a.tmp
```

```rollback
rm -f /tmp/agent-phase3-a.tmp
```

## Step: Create File B

```precheck
test ! -e /tmp/agent-phase3-b.tmp
```

```exec
touch /tmp/agent-phase3-b.tmp
```

```verify
test -f /tmp/agent-phase3-b.tmp
```

```rollback
rm -f /tmp/agent-phase3-b.tmp
```

## Step: Simulate Failure

```exec
false
```
