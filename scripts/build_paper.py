#!/usr/bin/env python3
"""Compile the paper from a fresh unpack of its TeX-source archive, then attach the byte-pinned replay ZIP to the reader PDF.
Requires pdfLaTeX (standard AMS, Latin Modern, microtype, booktabs, tabularx, geometry, graphics, hyperref) plus qpdf and the Poppler CLI.
TeX alone never reads the ancillary directory and does not need any tool or input from the finite replay.
"""
from pathlib import Path
import gzip, hashlib, io, os, shutil, subprocess, tarfile, tempfile
R=Path(__file__).resolve().parents[1];P=R/'paper';STAMP=1795046400;KIT='anc/no3-replay-r2.zip'
NAMES=('main.tex','proof.tex','collisions.tex','examples.tex','reproduction.tex','references.tex','table-ring.tex','table-other.tex','figures/one-flip.pdf',KIT);T=P/'arxiv-source.tar.gz'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
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
        assert sha(d/KIT) in (d/'reproduction.tex').read_text()
        env={**os.environ,'SOURCE_DATE_EPOCH':str(STAMP),'FORCE_SOURCE_DATE':'1','TZ':'UTC'}
        for i in range(3):
            p=subprocess.run(['pdflatex','-no-shell-escape','-halt-on-error','-file-line-error','-interaction=nonstopmode','main.tex'],cwd=d,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            if p.returncode:raise RuntimeError(p.stdout[-3500:])
        log=(d/'main.log').read_text();lines=[s for s in log.splitlines() if 'Warning:' in s or 'Overfull' in s or 'Underfull' in s]
        lines=[s for s in lines if s.strip()!='Package epstopdf Warning: Shell escape feature is not enabled.']
        if lines:raise RuntimeError('Unresolved typesetting diagnostics: '+'\n'.join(lines))
        print(next(s for s in log.splitlines() if s.startswith('Output written on')))
        def run(*args):return subprocess.check_output([str(z) for z in args],cwd=d,env=env)
        run('qpdf','--deterministic-id','main.pdf','--add-attachment',KIT,'--key='+Path(KIT).name,'--filename='+Path(KIT).name,'--mimetype=application/zip','--description=Finite coordinate certificates and replay code, revision R2','--creationdate=D:20261119000000Z','--moddate=D:20261119000000Z','--','reader.pdf')
        run('qpdf','--check','reader.pdf');assert Path(KIT).name.encode() in run('pdfdetach','-list','reader.pdf')
        run('pdfdetach','-save','1','-o','roundtrip.zip','reader.pdf');assert (d/'roundtrip.zip').read_bytes()==(d/KIT).read_bytes()
        assert run('pdftotext','main.pdf','-')==run('pdftotext','reader.pdf','-')
        shutil.copyfile(d/'reader.pdf',P/'main.pdf');shutil.copyfile(a,T)
    print(f'PASS fresh source-archive build: {len(NAMES)} members, one LaTeX root, clean three-pass pdfLaTeX build.');print('PASS reader PDF attachment round trip, SHA256',sha(P/KIT));print('arxiv-source.tar.gz SHA256',sha(T));print('main.pdf SHA256',sha(P/'main.pdf'))
if __name__=='__main__':build()
