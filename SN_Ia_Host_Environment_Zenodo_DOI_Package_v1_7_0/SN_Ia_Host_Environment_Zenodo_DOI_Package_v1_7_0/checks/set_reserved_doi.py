#!/usr/bin/env python
from pathlib import Path
import re, sys, json, subprocess
ROOT=Path(__file__).resolve().parents[1]
if len(sys.argv)!=2 or not re.fullmatch(r'10\.5281/zenodo\.\d+',sys.argv[1]):
 raise SystemExit('Usage: python checks/set_reserved_doi.py 10.5281/zenodo.XXXXXXX')
doi=sys.argv[1]
files=[ROOT/'README.md',ROOT/'CITATION.cff',ROOT/'codemeta.json',ROOT/'metadata/zenodo_metadata.json',ROOT/'metadata/release_summary.json',ROOT/'metadata/version_lineage.json',ROOT/'RELEASE_NOTES.md']
for p in files:
 s=p.read_text(encoding='utf-8')
 s=s.replace('10.5281/zenodo.TBD',doi)
 p.write_text(s,encoding='utf-8')
subprocess.check_call([sys.executable,str(ROOT/'checks/build_manifest.py')])
subprocess.check_call([sys.executable,str(ROOT/'checks/verify_release.py')])
print(f'Inserted reserved DOI: {doi}')
