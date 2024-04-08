from typing import Union
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name ="static")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.get("/solutions")
async def solutions(request:Request):
    return templates.TemplateResponse("solutions.html",{"request":request})

@app.get("/research")
async def research(request:Request):
    return templates.TemplateResponse("research.html",{"request":request})

@app.get("/investment")
async def investment(request:Request):
    return templates.TemplateResponse("investment.html",{"request":request})