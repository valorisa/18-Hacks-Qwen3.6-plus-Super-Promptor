# Test File for py-mdlint

This is a test file with various markdown constructs to test the linter.

## Subheading Level 2

Some paragraph text here.

### Sub-subheading Level 3

More text content.

# Heading Level 1 ATX Style

This document tests various rules:

## Lists

* Item 1 with some content
- Item 2 with content
+ Item 3 with content

1. First numbered item
2. Second numbered item
3. Third numbered item

## Code Blocks

```python
def hello_world():
    print("Hello, World!")
    return 42
```

Inline `code` here.

## Links and Images

[Link to example](https://example.com)

![Alt text](image.png)

## Emphasis and Strong

This is *italic* and this is **bold** and this is ***bold italic***.

## Blockquotes

> This is a blockquote
> with multiple lines

## Tables

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

## Horizontal Rules

---

***

___

## HTML Inline

<span style="color:red">Red text</span>

<br>

## Spacing Issues

This has**no**space around emphasis markers.

This has * space * around emphasis.

## Long Lines That Exceed The Maximum Line Length Limit To Trigger MD013 Rule For Line Length Checking Purposes Only

## Multiple Spaces At Start Of Lines

  Indented text that should trigger rules.

## Trailing Whitespace

Trailing spaces at end of line here.   
More text.

## End of file without proper newline
