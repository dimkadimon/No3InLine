#!/usr/bin/env python3
"""Assemble the deterministic portable finite-data ZIP from an explicit allow-list.
No git, fetched inputs, TeX, search solver, binaries, or release-level hash cycle.
The rows of the TeX tables are golden text outputs in this ZIP, not ancillary TeX source files.
"""
from pathlib import Path
import hashlib, io, zipfile
R=Path(__file__).resolve().parents[1];DEST=R/'paper/anc/no3-replay-r2.zip'
FIXED='''LICENSE THIRD_PARTY.md
scripts/verify_release.py scripts/comparison.py scripts/restore_inputs.py scripts/audit_counting.py scripts/check_public_frames.py scripts/expand_ring.py
results/README.md results/source-register.csv results/lower-bounds.csv results/p22-crops.csv results/forum-counts.csv results/catalogue-index.csv
unbounded-gain/code/check_identities.py unbounded-gain/code/sample_root.py unbounded-gain/code/match_example.cpp unbounded-gain/code/verify_example.cpp
unbounded-gain/data/certificate.txt unbounded-gain/data/matching.txt unbounded-gain/data/verification.txt
small-prime-examples/check_ring.cpp small-prime-examples/examples.json small-prime-examples/verify.py
studies/improvements/SHA256SUMS studies/improvements/code/check_stream.cpp studies/improvements/code/verify_frame.cpp
studies/improvements/data/orbits293.csv studies/improvements/data/orbits389.csv
studies/larger-grids/SHA256SUMS studies/larger-grids/experiments/seedindex.json studies/larger-grids/data/edits_65537.txt studies/larger-grids/data/edits_500009.txt
studies/larger-grids/code/verify_small.py studies/larger-grids/data/d4-n67.json
studies/larger-grids/coordinates/d4-n67.csv studies/larger-grids/coordinates/d4-n69.csv
studies/followup/data/augmented4037.csv studies/no3research/SHA256SUMS
verification/counting-diagnostics.txt verification/comparisons.txt verification/source-pins.txt verification/p47-witnesses.txt verification/exported-rings.txt
'''.split()
def export():
    paths=FIXED[:]
    for p in (5,73,97,193,2521,3361,4201):
        paths.append(f'small-prime-examples/coordinates/p{p}.csv')
        if p!=5:paths.append(f'small-prime-examples/certificates/p{p}.txt')
    for n in (201,202):paths.extend((f'studies/larger-grids/coordinates/n{n}.csv',f'studies/larger-grids/data/extension-n{n}.json'))
    for n in (293,389,4037,10085,16018,32002,64006):paths.append(f'studies/improvements/coordinates/n{n}.csv')
    for p in (8009,16001,32003):paths.append(f'studies/improvements/data/final-{p}.txt')
    assert len(set(paths))==len(paths)
    files={name:(R/name).read_bytes() for name in paths};files['README.md']=(R/'replay/README.md').read_bytes()
    # The live results README describes a newer rendering; keep the R2 documentation in its ZIP.
    files['results/README.md']=(R/'replay/results-README-r2.md').read_bytes()
    for tag in ('ring','other'):files[f'paper/table-{tag}.txt']=(R/f'paper/table-{tag}.tex').read_bytes()
    files['MANIFEST.sha256']=''.join(f'{hashlib.sha256(files[n]).hexdigest()}  {n}\n' for n in sorted(files)).encode()
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in sorted(files):
            zi=zipfile.ZipInfo(name,(2026,11,19,0,0,0));zi.create_system=3;zi.external_attr=0o100644<<16
            z.writestr(zi,files[name],compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    payload=buf.getvalue();DEST.parent.mkdir(parents=True,exist_ok=True);DEST.write_bytes(payload)
    with zipfile.ZipFile(DEST) as z:
        assert z.testzip() is None and set(z.namelist())==set(files) and all(z.read(n)==files[n] for n in files)
    print('Replay ZIP:',len(files),'members,',len(payload),'bytes; SHA256',hashlib.sha256(payload).hexdigest())
if __name__=='__main__':export()
