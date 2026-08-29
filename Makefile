.PHONY: test test-containers lint release rehearse clean

test:
	python3 -m unittest -v tests.test_fairsem

test-containers:
	@for image in python:3.10-slim python:3.11-slim python:3.12-slim python:3.13-slim python:3.14-slim; do \
		echo "testing $$image"; \
		docker run --rm -v "$$PWD:/work" -w /work "$$image" python3 -m unittest -v tests.test_fairsem || exit 1; \
	done

lint:
	python3 -m py_compile bin/fairsem tests/test_fairsem.py tests/helpers/*.py scripts/*.py
	shellcheck install.sh uninstall.sh scripts/rehearse_release.sh

release:
	python3 scripts/build_release.py
	python3 scripts/check_release_metadata.py

rehearse: release
	./scripts/rehearse_release.sh

clean:
	rm -rf -- dist __pycache__ tests/__pycache__ tests/helpers/__pycache__ scripts/__pycache__
