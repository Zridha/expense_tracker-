# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.db.session import engine
from app.db.init_db import init_models
from app.api.v1 import auth, expenses, reports

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fixed: Remove /api/v1 prefix since it's already in the routers
app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(reports.router)

@app.on_event("startup")
async def on_startup():
    logger.info("Creating tables (dev/demo mode)…")
    await init_models(engine)

@app.get("/")
async def root():
    return {"status": "ok", "app": settings.APP_NAME}