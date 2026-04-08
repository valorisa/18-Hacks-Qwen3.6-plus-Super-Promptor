from markdown_it import MarkdownIt

md = MarkdownIt()
content = """Text

```python
code
```

More
"""
tokens = md.parse(content)
for t in tokens:
    print(f'{t.type:30s} info={t.info!r:15s} tag={t.tag!r:10s} map={t.map}')
