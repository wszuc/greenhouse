#!/bin/bash
cd /home/wiktor/Desktop/greenhouse
source bin/activate
killall libgpiod_pulsein
PYTHONPATH=. python app/scripts/record_temp.py
