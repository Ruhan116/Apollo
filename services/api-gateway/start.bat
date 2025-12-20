@echo off
echo Starting API Gateway on port 8000...
set PYTHONPATH=D:\Win\Apollo
cd /d D:\Win\Apollo\services\api-gateway
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
