uvicorn main:app --host 0.0.0.0 --port 8000 &

sleep 5

ngrok http 8000
