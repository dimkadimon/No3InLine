PYTHON ?= python3
export PYTHONDONTWRITEBYTECODE := 1
.PHONY: check hashes table paper inputs replay counting public-frames diagrams legacy scales
check:
	$(PYTHON) scripts/verify_release.py
hashes:
	$(PYTHON) scripts/verify_release.py --hashes-only
table:
	$(PYTHON) scripts/comparison.py
	$(PYTHON) scripts/review_tables.py
scales:
	$(PYTHON) paper/anc/check-scales.py
paper:
	$(PYTHON) scripts/build_paper.py
inputs:
	$(PYTHON) scripts/restore_inputs.py --fetch
legacy:
	$(PYTHON) scripts/verify_release.py --expand-large
	$(PYTHON) scripts/comparison.py --audit-sources
	$(PYTHON) studies/improvements/verify.py --rescan
	$(PYTHON) studies/larger-grids/verify.py

replay:
	$(PYTHON) scripts/package_replay.py
counting:
	$(PYTHON) scripts/audit_counting.py
public-frames:
	$(PYTHON) scripts/check_public_frames.py

diagrams:
	$(PYTHON) scripts/construction_diagrams.py --previews paper/figures/previews
