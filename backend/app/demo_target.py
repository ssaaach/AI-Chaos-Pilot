"""Separate real HTTP target. Read-only; there is no fault execution endpoint."""
import time
from threading import Lock
from fastapi import FastAPI
app=FastAPI(title="Local demo target",docs_url=None,redoc_url=None,openapi_url=None)
started=time.monotonic()
requests=0
lock=Lock()
@app.get("/health")
def health():
    global requests
    with lock:
        requests+=1
        return {"status":"healthy","service":"demo-target","requests":requests,"mutations_received":0,"uptime_seconds":round(time.monotonic()-started,3)}
