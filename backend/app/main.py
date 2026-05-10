import asyncio
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import alerts, auth, heatmap, stream
from app.websocket.alerts import router as ws_router


app = FastAPI(
    title="GLOF Sentinel API",
    version="1.0.0",
    description="Early warning backend for glacier lake outburst flood prediction and evacuation alerts.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def enforce_response_budget(request, call_next):
    started = time.perf_counter()
    try:
        response = await asyncio.wait_for(call_next(request), timeout=5.0)
    except asyncio.TimeoutError:
        return JSONResponse(status_code=504, content={"detail": "Request exceeded 5 second SLA"})
    response.headers["X-Process-Time"] = f"{time.perf_counter() - started:.4f}"
    return response

app.include_router(auth.router, prefix="/api")
app.include_router(stream.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(heatmap.router, prefix="/api")
app.include_router(ws_router)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
