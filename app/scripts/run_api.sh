#!/bin/bash
cd /home/wiktor/Desktop/greenhouse
source bin/activate
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000
