#!/bin/bash

pip install -U arrow
pip install -r requirements.txt

for file in sample_input/*
do
	python -m geektrust "$file"
	python -m unittest discover
	coverage run --omit='/usr/*' -m unittest discover
	coverage report -m
done

