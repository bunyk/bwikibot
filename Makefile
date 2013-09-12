test:
	python3 test.py
	python test.py

version:
	rm -rf dist
	python3 next_version.py
	python3 setup.py register sdist upload
	hg addremove
