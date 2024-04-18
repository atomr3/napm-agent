from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.routing import APIRoute
import os
import psutil


'''
Bash: uvicorn main:app --reload
Comment in/out code: Ctrl + "/"

Requirements:
- fastapi
- uvicorn
- psutil
'''

app = FastAPI()

router = APIRouter()

@router.get("/")
async def Sitemap(request: Request):
    routes = app.routes
    valid_pages = []
    for route in routes:
        if isinstance(route, APIRoute) and route.path != "/":
            valid_pages.append(route.path) #route.name gets the name of the functions
    
    bullet_list = "<ul>" + "".join([f"<li><a href='{path}'>{path}</a></li>" for path in valid_pages]) + "</ul>"
    html_content = f"<h1>Valid Pages:</h1>{bullet_list}"
    return HTMLResponse(content=html_content)

@app.get("/plot/cpu-usage")
async def Cpu_Usage_Plot():
    html_file_path = os.path.join(os.path.dirname(__file__), "templates/cpu-history.html")
    return FileResponse(html_file_path)

@app.get("/cpu-usage")
async def get_cpu_usage():
    return {"cpu_usage_percent": psutil.cpu_percent(interval=1)}

app.include_router(router)