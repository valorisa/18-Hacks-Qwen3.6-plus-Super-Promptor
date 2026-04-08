from py_mdlint.parser import parse_markdown

content = """Text

```python
code
```

More
"""
tokens, lines = parse_markdown(content)
for t in tokens:
    print(f'{t.type:30s} info={t.meta.get("info", "")!r:15s} tag={t.tag!r:10s}')
