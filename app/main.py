from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from contextlib import asynccontextmanager
from app.db import init_db, create_url, get_url, get_analytics_by_code, gen

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app=FastAPI(lifespan=lifespan)

class URLRequest(BaseModel):
    url: HttpUrl
    custom_alias: str=None

class AnalyticsItem(BaseModel):
    code: str
    url: str
    clicks: int

@app.get("/health")
def health():
    return {"ok":True}

@app.post("/shorten")
def shorten(req: URLRequest):
    code=req.custom_alias or gen()
    if len(code)>10:
        raise HTTPException(400,"Too long")
    if not create_url(str(req.url),code):
        raise HTTPException(409,"Exists")
    return {"short_url":f"/{code}"}

@app.get("/{code}")
def redirect(code: str):
    url=get_url(code)
    if not url:
        raise HTTPException(404)
    return RedirectResponse(url)

@app.get("/analytics/{code}", response_model=AnalyticsItem)
def analytics(code: str):
    d=get_analytics_by_code(code)
    if not d:
        raise HTTPException(404)
    return d