import re


_TABLE_ENVIRONMENT_PATTERN = re.compile(
    r'\\begin\{(?P<environment>'
    r'array|matrix|pmatrix|bmatrix|Bmatrix|vmatrix|Vmatrix|smallmatrix|'
    r'aligned|alignedat|gathered|cases'
    r')\}(?P<body>[\s\S]*?)\\end\{(?P=environment)\}'
)

# A lone backslash followed by a likely row start is a common copy/paste error.
# Keep the rule deliberately narrow so valid commands such as \frac, \left,
# \alpha, \quad, and spacing commands remain untouched.
_LIKELY_SINGLE_ROW_SEPARATOR_PATTERN = re.compile(
    r'(?<!\\)\\(?!\\)(?=(?:\d|[xyzXYZ]\s*[&=+\-]))'
)


def repair_common_katex_input(raw_value):
    """Repair a small set of unambiguous/common KaTeX input mistakes."""
    content = str(raw_value or '')
    if not content:
        return ''

    # ``\left`` and ``\right`` require a delimiter. A literal brace must be
    # escaped; the unescaped variants below are always invalid KaTeX.
    content = content.replace(r'\left{', r'\left\{')
    content = content.replace(r'\right}', r'\right\}')

    def repair_table_environment(match):
        return _LIKELY_SINGLE_ROW_SEPARATOR_PATTERN.sub(
            lambda _separator: r'\\',
            match.group(0),
        )

    return _TABLE_ENVIRONMENT_PATTERN.sub(repair_table_environment, content)
