#!/usr/bin/env python3
"""Compile the paper from a fresh unpack of its TeX-source archive, then attach the byte-pinned replay ZIP to the reader PDF.
Requires pdfLaTeX (standard AMS, Latin Modern, microtype, booktabs, tabularx, geometry, graphics, hyperref) plus qpdf and the Poppler CLI.
TeX alone never reads the ancillary directory and does not need any tool or input from the finite replay.
"""
from pathlib import Path
import csv, gzip, hashlib, io, json, os, re, shutil, subprocess, sys, tarfile, tempfile
R=Path(__file__).resolve().parents[1];P=R/'paper';STAMP=1795046400;KIT='anc/no3-replay-r2.zip'
NAMES=('main.tex','proof.tex','collisions.tex','constants.tex','examples.tex','references.tex','table-checked-ring.tex','table-other.tex','table-reports.tex','figures/one-flip.pdf','figures/ring-and-masks.pdf','figures/matched-secants.pdf','figures/shared-level-selection.pdf','anc/README.txt','anc/check-scales.py',KIT);T=P/'arxiv-source.tar.gz'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build():
    subprocess.run([sys.executable, R/'scripts/review_tables.py'],check=True)
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
        assert b'PASS exact matrix and cyclotomic arithmetic' in run(sys.executable,'anc/check-scales.py')
        run('qpdf','--deterministic-id','main.pdf','--add-attachment',KIT,'--key='+Path(KIT).name,'--filename='+Path(KIT).name,'--mimetype=application/zip','--description=Finite coordinate certificates and replay code, revision R2','--creationdate=D:20261119000000Z','--moddate=D:20261119000000Z','--','reader.pdf')
        run('qpdf','--check','reader.pdf');assert Path(KIT).name.encode() in run('pdfdetach','-list','reader.pdf')
        run('pdfdetach','-save','1','-o','roundtrip.zip','reader.pdf');assert (d/'roundtrip.zip').read_bytes()==(d/KIT).read_bytes()
        assert run('pdftotext','main.pdf','-')==run('pdftotext','reader.pdf','-')
        text=run('pdftotext','-layout','reader.pdf','-').decode();front=text.split('\f')[0]
        for gone in ('Mathematics Subject Classification','Keywords.','Appendix B','Data availability and replay','??'):assert gone not in text,gone
        assert 'November' not in front and 'Dmitry Kamenetsky' in front
        repo='https://github.com/dimkadimon/No3InLine'
        intro_title='How the construction works'
        parts=re.split(r'(?m)^\s*1\s+'+re.escape(intro_title)+r'\s*$',front)
        assert len(parts)==2, 'The page-one introduction should start with the construction.'
        abstract=parts[0].split('Abstract',1)[1]
        assert abstract.rstrip().endswith(repo+'.'), 'The abstract must end with the repository URL.'
        assert re.search(r'(?m)^ *1 +Annotation +'+re.escape(repo)+r' *$',run('pdfinfo','-url','reader.pdf').decode()), 'Missing page-one repository link.'
        for fragment in ('2^(-s) product_', '0 <= R_A <= s/2', 'nonempty J in powerset', '(1/4) * 2^(-131) = 2^(-133)', 'lim (n -> infinity, n in N)', 'F_ht(n) - 3n/2', 'L_p^5/I^(1/4)', 'N/L_p^6'):assert fragment in text,fragment
        print('PASS abstract ends with a clickable page-one repository URL; extracted limit and probability bound preserve the subsequence and exponents.')
        flat=' '.join(text.split())
        abstract_flat=' '.join(abstract.split())
        assert abstract_flat.startswith('The no-three-in-line problem asks how many points') and 'no three lie on a straight line.' in abstract_flat[:160]
        assert 'super-polylogarithmic excess' in abstract_flat.lower()
        assert 'exp(log p / (114 log log p))' in abstract_flat and 'exp(log(p)/(114 log(log(p))))' in flat
        for fragment in ('hence d > x/(104 log x + 1).', 'log(p) >= 2^256 and log(I) >= log(p)/(105 log(log(p))).',
                         'log(2m) >= x/(105 log x) - 3 log L_p - 134 log 2 >= x/(114 log x).'):
            assert fragment in flat,fragment
        print('PASS problem-first abstract; Stewart conversion, explicit index test and exponent 114 in the reader.')
        assert '6(p-1) ring points + 8 anchors + 2m points from m opposite pairs = 6p + 2 + 2m.' in flat
        tour=[flat.index(h) for h in (intro_title,'Build the ring.','Flip a group.','Add an opposite pair.','From one pair to many.', 'Theorem 1.1.', 'A ring, eight anchors and a matching')]
        assert tour==sorted(tour) and tour[0]<flat.index('Figure 1: One flip')<tour[-2], 'The illustrated tour belongs before the formal theorem.'
        print('PASS illustrated ring, flip and added-pair walkthrough before Theorem 1.1.')
        body=flat[flat.index('What improves on the 1975 construction?'):]
        assert 'super-polylogarithmic excess' in body[:300] and 'If Theorem 1.1 is confirmed' in body[:550]
        for fragment in ('83,521 matrices','m >= c * min(I, sqrt(p)) / (L_p^3)', 'N = floor(J / (L_p^3))',
                         'p >= 2^276','m >= 2^(-135) min(I, sqrt(p)) / (L_p^3)', '2047314589905164660182861222233071665633201',
                         'Theorem 1.1, (1.7)', 'Theorem 1, (7)', 'Lemma 2.2'):
            assert fragment in flat,fragment
        assert '† Reported only.' in text and all(f'Figure {j}:' in text for j in range(1,5))
        headings=[' '.join(l.split()) for l in text.splitlines()]
        order=[headings.index(h) for h in ('Authorship and use of generative AI','References',
                                            'Construction and data sources','A Finite witnesses and comparisons')]
        assert order==sorted(order),order
        cells=[[v.replace(' ','') for v in re.split(r' {2,}',l.strip())] for l in text.splitlines()]
        rows=[c for c in cells if len(c)==7 and c[4] in ('H','Q','U')]
        with (R/'results/checked-comparisons.csv').open() as f: data=list(csv.DictReader(f))
        def signed(a):return f'{int(a):+d}'.replace('-','−')
        expected=[[r['n'],r['B_checked'],r['source_codes'],r['certified_count'],r['symmetry'],
                   signed(r['delta_vs_checked']),'+'+r['excess_vs_1.5n']] for r in data]
        assert sorted(rows)==sorted(expected),(rows,expected)
        reports=[c for c in cells if len(c)==7 and re.fullmatch(r'\[F[123]\]†',c[2])]
        assert [r[:2]+r[3:] for r in reports]==[[r['n'],r['report_source_side'],r['report_source_count'],
                    r['report_transfer'],r['certified_count'],signed(r['delta_vs_report'])] for r in data if r['report_transfer']],reports
        keys=re.findall(r'\\bibitem(?:\[[^]]+\])?\{([^}]+)\}',(d/'references.tex').read_text())
        dests={name:int(pg) for pg,name in re.findall(r'(?m)^ *(\d+) +\[.*?\] +"([^"]+)"',run('pdfinfo','-dests','reader.pdf').decode())}
        assert keys and all(dests[f'cite.{key}']<dests['appendix.A'] for key in keys)
        outline=json.loads(run('qpdf','--json','--json-key=outlines','reader.pdf'))['outlines']
        chapter=next(e for e in outline if e['title']==intro_title)
        result=next(e for e in chapter['kids'] if e['title']=='The excess above the classical bound')
        page=result['destpageposfrom1']
        assert page==dests['theorem.1.1']==dests['subsection.1.1'] and f'Theorem 1.1 on page {page}' in flat
        field=(P/'arxiv-abstract.txt').read_text(encoding='ascii').strip()
        assert 0<len(field)<=1920 and field.endswith(repo) and len(field.splitlines())==1
        src=(d/'main.tex').read_text().split(r'\begin{abstract}')[1].split(r'\end{abstract}')[0]
        pre,rest=src.split(r'\[');_,post=rest.split(r'\]')
        post=post.strip().replace(r'\emph{super-polylogarithmic excess}','super-polylogarithmic excess').replace(r'\mbox{\url{'+repo+'}}.',repo)
        assert field==' '.join([pre.strip(),r'$F_{\mathrm{ht}}(4p+1) \ge 6p+2+\exp(\log p/(114\log\log p))$.',post])
        print(f'PASS main result in PDF outline and forward page link; arXiv abstract {len(field)} ASCII characters with the manuscript text and denominator 114.')
        print(f'PASS reader: references and {len(keys)} citation destinations before Appendix A; both evidence tiers match the comparison CSV, including the two negative report differences.')
        assert b'https://raw.githubusercontent.com/dimkadimon/No3InLine/e19b8a1b689eba392c7d26ec3733e88db566dc0e/paper/anc/no3-replay-r2.zip' in run('pdfinfo','-url','reader.pdf')
        print('PASS reader: four figures, four marked report-only sources, clean formula extraction, requested removals and pinned kit link.')
        shutil.copyfile(d/'reader.pdf',P/'main.pdf');shutil.copyfile(a,T)
    print(f'PASS fresh source-archive build: {len(NAMES)} members, one LaTeX root, clean three-pass pdfLaTeX build.');print('PASS reader PDF attachment round trip, SHA256',sha(P/KIT));print('arxiv-source.tar.gz SHA256',sha(T));print('main.pdf SHA256',sha(P/'main.pdf'))
if __name__=='__main__':build()
