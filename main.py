import os
from typing import Union, Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile, File, Form
from generate import create_alttext

app = FastAPI()

class Item(BaseModel):
    text: str

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("/pages/index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("/pages/login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("/pages/signup.html", {"request": request})

@app.post("/")
async def alt_text(text: Annotated[str, Form()], img: UploadFile = File(...),):
    img_content = await img.read()
    img_path = f"images/{img.filename}"
    with open(img_path, "wb") as f:
        f.write(img_content)

    alt_text = create_alttext(text, img_path)

    return JSONResponse(content={
        "Generated Alt-Text": alt_text, 
    }) 

