_piptools := $(shell which pip-compile 2>/dev/null)

dev-install: requirements.txt
	python -m piptools sync requirements.txt
	
requirements.txt: pyproject.toml | setup-pip-tools
	pip-compile -o requirements.txt pyproject.toml
	
setup-pip-tools:
ifndef _piptools
	python -m pip install pip-tools
endif
	