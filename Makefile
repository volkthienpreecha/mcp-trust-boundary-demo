PYTHON ?= python

.PHONY: install unsafe safe-malicious safe-benign test

install:
	$(PYTHON) -m pip install -r requirements.txt

unsafe:
	$(PYTHON) -m demo.unsafe_client --config configs/malicious_demo.json

safe-malicious:
	$(PYTHON) -m demo.safe_client --config configs/malicious_demo.json

safe-benign:
	$(PYTHON) -m demo.safe_client --config configs/benign.json

test:
	$(PYTHON) -m pytest
