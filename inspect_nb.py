import json

nb = json.load(open(r'notebooks\02_Data_Preprocessing.ipynb', encoding='utf-8'))
cells = nb['cells']

for i, c in enumerate(cells):
    if c['cell_type'] == 'markdown':
        src = ''.join(c['source'])[:200]
        print(f"[MD {i}] {src}")
    elif c['cell_type'] == 'code':
        src = ''.join(c['source'])[:200]
        print(f"[CODE {i}] {src}")
