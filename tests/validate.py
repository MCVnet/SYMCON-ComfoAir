#!/usr/bin/env python3
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
def read(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))
lib = read('library.json')
mod = read('ZehnderQ350/module.json')
form = read('ZehnderQ350/form.json')
code = (ROOT/'ZehnderQ350/module.php').read_text(encoding='utf-8')
html = (ROOT/'ZehnderQ350/module.html').read_text(encoding='utf-8')
assert re.fullmatch(r'\{[A-F0-9-]{36}\}',lib['id'])
assert re.fullmatch(r'\{[A-F0-9-]{36}\}',mod['id'])
assert lib['id'] == '{DA63B40E-7893-4970-8ED3-DFCA09B24C31}'
assert mod['id'] == '{9C752C33-E59F-42AD-8F2E-601A26F921C0}'
assert lib['version'] == '1.0.0'
assert isinstance(lib['url'],str) and lib['url'].startswith('https://')
assert isinstance(mod['url'],str) and mod['url'].startswith('https://')
assert re.fullmatch(r'[A-Za-z0-9_ ]+',mod['name'])
cls=re.search(r'class\s+(\w+)\s+extends\s+IPSModule',code)
assert cls and cls.group(1)==mod['name'].replace(' ','')
assert mod['prefix']=='ZQ'
assert isinstance(form['elements'],list) and isinstance(form['actions'],list)
for method in ('Create','ApplyChanges','ReadSensors','RequestAction','GetVisualizationTile'):
    assert re.search(r'function\s+'+method+r'\s*\(',code), method
assert 'SetVisualizationType(1)' in code
assert 'requestAction(' in html and '__INITIAL_STATE__' in html
assert 'LiveWatchdog' not in code
print('OK: metadata, PHP class, required files, HTML tile and polling-only mode')
