import os

import uvicorn
from fastapi import FastAPI

from app.routers import index, health_check


app = FastAPI()

app.include_router(index.router)
app.include_router(health_check.router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
