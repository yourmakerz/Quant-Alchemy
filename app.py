from typing import Union
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from scripts import relative_strength, quantitative_analysis, treasuries
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
from typing import Union ,List, Optional


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
async def research(request:Request, symbol: Optional[str] = None):
    a,b = relative_strength.sector_strength()
    fig1  = px.line(a,x=a.index,y=a.columns)
    plot_html1 = fig1.to_html(full_html=False)
    fig = px.line(b,x=b.index,y=b.columns)
    plot_html2 = fig.to_html(full_html = False)
    
    if symbol is None:
        financial_health_html = ""
        valuation_html = ""
    else: 
        if isinstance(symbol, str):
            symbols = [symbol]
        elif isinstance(symbol, list):
            symbols = symbol
        else:
            raise ValueError("Symbol must be a string or a list of strings")
        financial_health_html = ""
        valuation_html = ""
        symbols = [i for x in symbols for i in x.replace(" ","").split(",")]
        print("------------------------------------------")
        print(symbols)
        
        rev_by_inv = quantitative_analysis.profitabilty(symbol=symbols)       
        financial_health, valuation = quantitative_analysis.get_company_data(symbol=symbols)

    # Generate bar graphs for financial health and valuation using Plotly
        financial_health_fig = px.bar(financial_health, x=financial_health.index, y=financial_health.columns,
                                labels={'x': 'Metrics', 'y': 'Values'}, title='Financial Health',log_y=True, barmode="group")
        valuation_fig = px.bar(valuation, x=valuation.index, y=valuation.columns,
                    labels={'x': 'Metrics', 'y': 'Values'}, title='Valuation', log_y=True,  barmode="group") 
        revByinv_fig = px.line(rev_by_inv, x="date", y=rev_by_inv.columns,labels={'x': 'Date', 'y': 'Revenue/Inventory'})
    # Convert the Plotly bar graphs to HTML code
        financial_health_html = financial_health_fig.to_html(full_html=False)
        valuation_html = valuation_fig.to_html(full_html=False)
        revByinv_fig_html = revByinv_fig.to_html(full_html=False)

    return templates.TemplateResponse("research.html",{"request":request,"plot1":plot_html1, "plot2":plot_html2,
                                                       "financial_health": financial_health_html,
                                                       "valuation": valuation_html,
                                                       "RevByInv": revByinv_fig_html})



@app.get("/research/yields")
async def yields(request: Request, selection: date = None):
    yields_data = treasuries.yields_data()
    print(f"----------------")
    print(f"{selection}")
    if selection is None:
        yield_html = ""
    else:
        # selection = selection.strftime("%Y-%m-%d")
        data = yields_data.loc[[selection]].T
        fig = px.line(data, x=data.index, y=selection)
        yield_html = fig.to_html(full_html=False)
    return templates.TemplateResponse("yields.html", {"request": request, "dates": yields_data.index, "yields_graph":yield_html})



@app.get("/investment")
async def investment(request:Request):
    return templates.TemplateResponse("investment.html",{"request":request})

