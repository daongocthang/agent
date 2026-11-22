
# Add Bin to PATH

Add ~/bin to PATH through ~/.bashrc.

## Step: Inject PATH

```exec
python3 scripts/injector.py add ~/.bashrc snippets/bin-path.sh
```

```verify
python3 scripts/injector.py check ~/.bashrc snippets/bin-path.sh
```

```rollback
python3 scripts/injector.py remove ~/.bashrc snippets/bin-path.sh
```

## Note

To apply changes to the current shell:

```bash
source ~/.bashrc
```
