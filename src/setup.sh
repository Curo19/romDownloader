#!/bin/bash
python3 -m venv romDownloader
source romDownloader/bin/activate
pip list
python3 -m pip install -r requirements.txt
pip list
cat requirements.txt
