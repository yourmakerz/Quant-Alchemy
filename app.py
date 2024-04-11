from typing import Union
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import relative_strength
import plotly.graph_objects as go
import plotly.express as px



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
    a,b = relative_strength.sector_strength()
    fig1  = go.Figure(data = go.Line(x=a.index,y=a.b_mark))
    plot_html1 = fig1.to_html(full_html=False)
    fig = px.line(b,x=b.index,y=b.columns)
    plot_html2 = fig.to_html(full_html = False)

    return templates.TemplateResponse("research.html",{"request":request,"plot1":plot_html1, "plot2":plot_html2})


@app.get("/investment")
async def investment(request:Request):
    return templates.TemplateResponse("investment.html",{"request":request})

