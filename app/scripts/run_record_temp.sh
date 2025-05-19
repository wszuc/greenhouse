#!/bin/bash
cd /home/wiktor/Desktop/greenhouse
source bin/activate
PYTHONPATH=. python app/scripts/record_temp.py
