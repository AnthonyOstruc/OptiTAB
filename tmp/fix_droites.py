filepath = '/Users/anthonytabet/Desktop/OptiTABV3/frontend/exercices/2nd/exercice_droites_plan_seconde.txt'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the exact text to replace
search = ('    \u25cf **R\u00e9sultat :** La fonction renvoie <code>(-6, 6, -6)</code> et l\u2019\u00e9quation est $\\displaystyle x-y+1=0$\n'
          '    $\\\\$\n'
          '\n'
          '**Question 4 :** Cas $\\displaystyle A=B$')

replace = ('    \u25cf **R\u00e9sultat :** La fonction renvoie <code>(-6, 6, -6)</code> et l\u2019\u00e9quation est $\\displaystyle x-y+1=0$\n'
           '    $\\\\$\n'
           '    \u25cf **Remarque :** Le triplet $\\displaystyle (a,b,c)$ n\u2019est pas unique\u00a0: tout multiple non nul $\\displaystyle (ka,kb,kc)$ d\u00e9crit la m\u00eame droite. Par exemple <code>(-6, 6, -6)</code> et <code>(1, -1, 1)</code> donnent toutes les deux la droite $\\displaystyle x-y+1=0$.\n'
           '    $\\\\$\n'
           '\n'
           '**Question 4 :** Cas $\\displaystyle A=B$')

if search in content:
    content = content.replace(search, replace, 1)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS")
else:
    print("NOT FOUND - searching for surrounding text...")
    idx = content.find('<code>(-6, 6, -6)</code>')
    if idx >= 0:
        print(repr(content[idx-5:idx+150]))
    else:
        print("Cannot find the code block either")
