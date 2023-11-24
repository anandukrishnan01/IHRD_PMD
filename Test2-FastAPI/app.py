from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import json
import random
from datetime import datetime
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Route to serve the HTML template
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Streaming endpoint to send dummy data to the chart
@app.get("/chart-data")
async def chart_data(request: Request) -> StreamingResponse:
    response = StreamingResponse(generate_dummy_data(), media_type="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

# Function to generate dummy data
async def generate_dummy_data() -> str:
    while True:
        json_data = json.dumps(
            {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "value": random.random() * 100,
            }
        )
        yield f"data:{json_data}\n\n"
        await asyncio.sleep(1)
