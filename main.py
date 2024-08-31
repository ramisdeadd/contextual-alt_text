import os
from typing import Union, Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import UploadFile, File, Form, HTTPException, status
from generate import create_alttext

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johnsmith": {
        "username": "johnsmith",
        "full_name": "John Smith",
        "email": "johnsmith@gmail.com",
        "hashed_password": "fakehashedsecret1",
        "disabled": False,
    },
    "ryanbang": {
        "username": "ryanbang",
        "full_name": "Ryan Bang",
        "email": "ryanbang@gmail.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    }
}

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str


def fake_hash_password(password: str):
    return "fakehashed" + password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authentication Credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user

@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect Username or Password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect Username or Password")

    return {"access_token": user.username, "token_type": "bearer"}

########

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("/pages/index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("/pages/login.html", {"request": request})

@app.post("/")
async def alt_text(text: Annotated[str, Form()], img: UploadFile = File(...)):
    img_content = await img.read()
    img_path = f"images/{img.filename}"
    with open(img_path, "wb") as f:
        f.write(img_content)

    alt_text = create_alttext(text, img_path)

    return JSONResponse(content={
        "Generated Alt-Text": alt_text, 
    }) 
