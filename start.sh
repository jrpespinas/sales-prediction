#!/bin/sh
# Use the following for local testing, comment on deployment
# uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers 4

# Use the following for deployment, comment on local
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4