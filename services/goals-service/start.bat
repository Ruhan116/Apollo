@echo off
echo Starting Goals Service on port 8002...
set PYTHONPATH=D:\Win\Apollo
cd /d D:\Win\Apollo\services\goals-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
