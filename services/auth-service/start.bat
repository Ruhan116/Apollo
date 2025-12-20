@echo off
echo Starting Auth Service on port 8001...
set PYTHONPATH=D:\Win\Apollo
cd /d D:\Win\Apollo\services\auth-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
