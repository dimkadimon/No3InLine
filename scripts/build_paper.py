#!/usr/bin/env python3
"""Build the arXiv source archive, then compile the paper FROM THAT ARCHIVE in a clean directory.
Needs pdflatex with the standard AMS, Latin Modern, microtype, booktabs, geometry, graphics and hyperref packages.
"""
from pathlib import Path
import gzip, hashlib, io, os, shutil, subprocess, tarfile, tempfile
R=Path(__file__).resolve().parents[1];P=R/'paper';STAMP=1795046400
NAMES=('main.tex','proof.tex','examples.tex','references.tex','table-ring.tex','table-other.tex','figures/one-flip.pdf');T=P/'arxiv-source.tar.gz'
def build():
    with tempfile.TemporaryDirectory() as tmp:
        d=Path(tmp);a=d/T.name
        with a.open('wb') as f,gzip.GzipFile(fileobj=f,mode='wb',filename='',mtime=STAMP) as g,tarfile.open(fileobj=g,mode='w') as t:
            for n in NAMES:
                b=(P/n).read_bytes();v=tarfile.TarInfo(n);v.size=len(b);v.mode=0o644;v.mtime=STAMP;t.addfile(v,io.BytesIO(b))
        with tarfile.open(a,'r:gz') as t:
            assert tuple(t.getnames())==NAMES
            for n in NAMES:
                q=d/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(t.extractfile(n).read());assert q.read_bytes()==(P/n).read_bytes()
        env={**os.environ,'SOURCE_DATE_EPOCH':str(STAMP),'FORCE_SOURCE_DATE':'1','TZ':'UTC'}
        for i in range(3):
            p=subprocess.run(['pdflatex','-no-shell-escape','-halt-on-error','-file-line-error','-interaction=nonstopmode','main.tex'],cwd=d,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            if p.returncode:raise RuntimeError(p.stdout[-3500:])
        log=(d/'main.log').read_text();lines=[s for s in log.splitlines() if 'Warning:' in s or 'Overfull' in s or 'Underfull' in s];
        lines=[s for s in lines if s.strip()!='Package epstopdf Warning: Shell escape feature is not enabled.']  # expected: PDF-only, no shell escape
        if lines:raise RuntimeError('Unresolved typesetting diagnostics: '+'\n'.join(lines))
        print(next(s for s in log.splitlines() if s.startswith('Output written on')));shutil.copyfile(d/'main.pdf',P/'main.pdf');shutil.copyfile(a,T)
    print('PASS source-only archive: seven files, one LaTeX root, figure present, clean three-pass pdfLaTeX build.');print('arxiv-source.tar.gz SHA256',hashlib.sha256(T.read_bytes()).hexdigest())
if __name__=='__main__':build()
