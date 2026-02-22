import re
import sys

filepath = 'frontend/exercices/2nd/exercice_droites_plan_seconde.txt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match $...$ but not $$...$$
pattern = re.compile(r'(?<!\$)\$(?!\$)([^$]+?)\$(?!\$)')

skip_tags = ['style=', '<span', '<code>', '<td', '<tr', '<table']

lines = content.split('\n')
new_lines = []
total_fixed = 0

for line in lines:
    # Skip HTML lines
    if any(tag in line for tag in skip_tags):
        new_lines.append(line)
        continue

    def replacer(m):
        global total_fixed
        inner = m.group(1)
        # Already has displaystyle
        if 'displaystyle' in inner:
            return m.group(0)
        # Skip line breaks $\\$
        stripped = inner.strip()
        if stripped == '\\\\':
            return m.group(0)
        # Skip $\qquad$
        if stripped == '\\qquad':
            return m.group(0)
        if not stripped:
            return m.group(0)
        total_fixed += 1
        return '$\\displaystyle ' + inner + '$'

    new_line = pattern.sub(replacer, line)
    new_lines.append(new_line)

new_content = '\n'.join(new_lines)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Fixed {total_fixed} formulas")
