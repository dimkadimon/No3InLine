#!/usr/bin/env python3
"""Compile the paper from a fresh unpack of its TeX-source archive, then attach the byte-pinned replay ZIP to the reader PDF.
Requires pdfLaTeX (standard AMS, Latin Modern, microtype, booktabs, tabularx, geometry, graphics, hyperref) plus qpdf and the Poppler CLI.
TeX alone never reads the ancillary directory and does not need any tool or input from the finite replay.
"""
from pathlib import Path
import gzip, hashlib, io, os, re, shutil, subprocess, tarfile, tempfile
R=Path(__file__).resolve().parents[1];P=R/'paper';STAMP=1795046400;KIT='anc/no3-replay-r2.zip'
NAMES=('main.tex','proof.tex','collisions.tex','examples.tex','references.tex','table-ring.tex','table-other.tex','figures/one-flip.pdf','figures/ring-and-masks.pdf','figures/matched-secants.pdf','figures/shared-level-selection.pdf','anc/README.txt',KIT);T=P/'arxiv-source.tar.gz'
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
        assert sha(d/KIT) in (d/'anc/README.txt').read_text()
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
        text=run('pdftotext','-layout','reader.pdf','-').decode();front=text.split('\f')[0]
        for gone in ('Mathematics Subject Classification','Keywords.','Appendix B','Data availability and replay','??'):assert gone not in text,gone
        assert 'November' not in front and 'Dmitry Kamenetsky' in front
        for fragment in ('2^(-s) product_', '0 <= R_A <= s/2', 'nonempty J in powerset', 'F_ht(n) - 3n/2', 'L_p^5/I^(1/4)', 'N/L_p^6'):assert fragment in text,fragment
        cells=[re.split(r' {2,}',l.strip()) for l in text.splitlines()]
        marked=[c[0].replace(' ','') for c in cells if len(c)>2 and c[2]=='F†']
        assert marked==['293','389','773','4037'],marked
        assert '† Reported only.' in text and all(f'Figure {j}:' in text for j in range(1,5))
        headings=[' '.join(l.split()) for l in text.splitlines()]
        order=[headings.index(h) for h in ('Authorship and use of generative AI','References',
                                            'Construction and data sources','A Finite witnesses and comparisons')]
        assert order==sorted(order),order
        rows=[[v.replace(' ','') for v in c] for c in cells if len(c)==7 and re.fullmatch(r'[0-9][0-9 ]*',c[0])]
        assert len(rows)==15,len(rows)
        assert [r for r in rows if r[-2].startswith('−')]==[
            ['293','512','F†','508','Q','−4','+68.5'],['773','1244','F†','1188','H','−56','+28.5']]
        keys=re.findall(r'\\bibitem(?:\[[^]]+\])?\{([^}]+)\}',(d/'references.tex').read_text())
        dests={name:int(pg) for pg,name in re.findall(r'(?m)^ *(\d+) +\[.*?\] +"([^"]+)"',run('pdfinfo','-dests','reader.pdf').decode())}
        assert keys and all(dests[f'cite.{key}']<dests['appendix.A'] for key in keys)
        print(f'PASS reader: references and {len(keys)} citation destinations before Appendix A; both negative rows and their positive excesses.')
        assert b'https://raw.githubusercontent.com/dimkadimon/No3InLine/e19b8a1b689eba392c7d26ec3733e88db566dc0e/paper/anc/no3-replay-r2.zip' in run('pdfinfo','-url','reader.pdf')
        print('PASS reader: four figures, four F-dagger source cells, clean formula extraction, requested removals and pinned kit link.')
        shutil.copyfile(d/'reader.pdf',P/'main.pdf');shutil.copyfile(a,T)
    print(f'PASS fresh source-archive build: {len(NAMES)} members, one LaTeX root, clean three-pass pdfLaTeX build.');print('PASS reader PDF attachment round trip, SHA256',sha(P/KIT));print('arxiv-source.tar.gz SHA256',sha(T));print('main.pdf SHA256',sha(P/'main.pdf'))
if __name__=='__main__':build()
