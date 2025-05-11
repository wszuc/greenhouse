#!/bin/bash
cd /home/wiktor/Desktop/greenhouse
source bin/activate
PYTHONPATH=. fastapi dev app/main.py --host 0.0.0.0 --port 8000
