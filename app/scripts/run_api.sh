#!/bin/bash
cd /home/pi/twoj_projekt
source venv/bin/activate
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000
