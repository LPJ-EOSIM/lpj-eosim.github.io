# Add A Version

Add one page per model revision and name the nav entry after the PR or commit the outputs came from.

Suggested labels:

- `PR #123`
- `commit abc1234`

Suggested file layout:

```text
docs/
  assets/
    results/
      pr-123/
        figure-1.png
        figure-2.png
  results/
    pr-123.md
```

Suggested nav entry in `mkdocs.yml`:

```yaml
- Results:
    - Overview: results/index.md
    - ILAMB Benchmark: results/current-ilamb.md
    - PR #123: results/pr-123.md
```

Minimal page template:

```md
# PR #123

Model source: `owner/repo@abc1234`

Pull request: `#123`

![Result figure 1](../../assets/results/pr-123/figure-1.png)
![Result figure 2](../../assets/results/pr-123/figure-2.png)
```
