
# Test Agent

Kiểm tra workflow Precheck → Execute → Verify.

## Step: Check Kernel

```precheck
test -r /proc/version
```

```exec
uname -r
```

```verify
test -r /proc/version
```

## Step: Check Memory

```precheck
test -r /proc/meminfo
```

```exec
free -h
```

```verify
test -r /proc/meminfo
```

## Step: Check Disk

```precheck
test -d /
```

```exec
df -h /
```

```verify
test -d /
```
