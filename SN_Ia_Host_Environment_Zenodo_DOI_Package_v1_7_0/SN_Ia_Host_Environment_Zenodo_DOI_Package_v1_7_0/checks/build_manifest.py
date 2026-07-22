#!/usr/bin/env python
from pathlib import Path
import hashlib, pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'metadata/file_manifest_sha256.csv'
EXCLUDED={'metadata/file_manifest_sha256.csv','docs/verification_report.txt'}
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
 return h.hexdigest()
rows=[]
for p in sorted(ROOT.rglob('*')):
 if p.is_file():
  rel=p.relative_to(ROOT).as_posix()
  if rel not in EXCLUDED: rows.append({'relative_path':rel,'size_bytes':p.stat().st_size,'sha256':digest(p)})
pd.DataFrame(rows).to_csv(OUT,index=False)
print(f'Wrote {OUT} with {len(rows)} entries.')
