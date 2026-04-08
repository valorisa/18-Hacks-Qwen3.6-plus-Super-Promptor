# tests/conftest.py
"""Fixtures pytest partagées."""

import pytest
from py_mdlint.registry import load_rules
from py_mdlint.parser import parse_markdown


@pytest.fixture
def run_rule():
    """
    Helper: exécute une règle contre du contenu Markdown.
    
    Usage:
        violations = run_rule("MD001", "# Title\n\n### Subtitle")
    """
    def _run(rule_id: str, markdown: str, config: dict = None):
        rules = load_rules()
        if rule_id not in rules:
            pytest.fail(f"Rule {rule_id} not found in registry")

        rule = rules[rule_id]
        rule.params = dict(config or {})
        tokens, lines = parse_markdown(markdown)
        return rule.check(tokens, lines, config or {})
    
    return _run


@pytest.fixture
def sample_markdown():
    """Contenu Markdown de test avec violations variées."""
    return """# Title

## Valid subsection

### Valid sub-subsection

# Another H1 after H3 - MD001 violation

Text with trailing spaces   

- List item
  - Nested with wrong indent  # MD007 if indent=2

[Broken link](  )  # MD011 if spaces in link

```python
# Code block
```

<details>
<summary>HTML inline</summary>
Content
</details>
"""
