init:
	pip3 install -r requirements.txt

demon:
	python3 yasdidemon.py

test:
	python3 -m unittest discover
