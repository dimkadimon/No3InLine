PYTHON ?= python3
export PYTHONDONTWRITEBYTECODE := 1
.PHONY: check hashes table paper inputs legacy
check:
	$(PYTHON) scripts/verify_release.py
hashes:
	$(PYTHON) scripts/verify_release.py --hashes-only
table:
	$(PYTHON) scripts/comparison.py
paper:
	$(PYTHON) scripts/build_paper.py
inputs:
	$(PYTHON) scripts/restore_inputs.py --fetch
legacy:
	$(PYTHON) scripts/verify_release.py --expand-large
	$(PYTHON) scripts/comparison.py --audit-sources
	$(PYTHON) studies/improvements/verify.py --rescan
	$(PYTHON) studies/larger-grids/verify.py
