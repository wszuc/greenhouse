#!/bin/bash
cd /home/pi/twoj_projekt
source venv/bin/activate
PYTHONPATH=. python app/scripts/record_temp.py
