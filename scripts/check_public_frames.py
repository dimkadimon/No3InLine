#!/usr/bin/env python3
"""Recheck the three public P47 baselines from their own pinned addition lists (restore_inputs.py --group station).
The input is converted to a zero-removal edit script; the project checker checks the frame and all triples touching additions.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib, os, shlex, subprocess, sys
R=Path(__file__).resolve().parents[1];I=R/'studies/improvements'
if not __debug__:sys.exit('Do not use python -O')
with TemporaryDirectory() as tmp:
    w=Path(tmp);exe=w/'check';subprocess.run(shlex.split(os.environ.get('CXX','c++'))+['-O3','-std=c++17',str(I/'code/verify_frame.cpp'),'-o',str(exe)],check=True)
    digests={b:a for a,b in (s.split('  ',1) for s in (I/'SHA256SUMS').read_text().splitlines())}
    for p,m in ((8009,282),(16001,421),(32003,810)):
        f=f'sources/insertions_{p}.txt';raw=(I/f).read_bytes();assert hashlib.sha256(raw).hexdigest()==digests[f];header,body=raw.decode().split('\n',1);assert list(map(int,header.split()))==[p,m];q=w/'edits.txt';q.write_text(f'{p} 0 {m}\n'+body)
        s=subprocess.check_output([exe,q],text=True);assert f' total={3*(p-1)+m} ' in s;print(s,end='',flush=True)
print('PASS: all three public P47 v1 point sets reconstructed from the source additions and checked as ordinary caps.')
