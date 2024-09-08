import os
import json
from datetime import datetime, timedelta, timezone
from typing import Union, Annotated

import jwt
import uvicorn
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import Column, Integer
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, UploadFile, File, Form, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from generate import create_alttext

SECRET_KEY = "aafb48d530ee71c753e64e6830439b026c9405685c19b8829b8065c881ad2876"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "ryanbang": {
        "username": "ryanbang",
        "email": "ryanbang@gmail.com",
        "hashed_password": "f3d600bd00b0ce715b50e189dd34d7f12c0bb7173ae49c380cdecae5c74bb279",
        "disabled": True,
    }
}

class UserBase(SQLModel):
    username: str = Field(index=True)
    email: str = Field(unique=True)
    disabled: bool = Field(default=False)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    hashed_password: str

class UserPublic(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Temporary
class UserInDB(User):
    hashed_password: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Server ....")
    create_db_and_tables()
    yield
    print("Stopping Server ....")

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

sqlite_file_name = "alt-text.db"
sqlite_url = f"sqlite:///../data/{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)

def get_user(username: str):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        result = session.exec(statement)
        user = result.first()
        return user

def authenticate_user(username: str, plain_password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(plain_password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user

@app.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # login_for_access_token -> authenticate_user -> get_user -> verify_password -> END
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # create_access_token -> END
    access_token = create_access_token(
        data = {"sub": user.username}, 
        expires_delta = access_token_expires
    )
    print("Succesful Login")
    return Token(access_token=access_token, token_type="bearer")

# read_users_me -> get_current_active_user -> get_current_user -> get_user
@app.get("/users/me", response_model = User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

########

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("/pages/index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("/pages/login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("/pages/signup.html", {"request": request})

@app.post("/signup", response_model=UserPublic)
async def signup_user(username: Annotated[str, Form()], email: Annotated[str, Form()], plain_password: Annotated[str, Form()]):
    hashed_password = get_password_hash(plain_password)
    user = UserCreate(
        username = username,
        email = email,
        hashed_password = hashed_password,
        disabled = False,
    )
    user = await create_user(user)
    return user

async def create_user(user: Annotated[UserCreate, Depends(signup_user)]):
    with Session(engine) as session:
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    print(f"Succesful Signup")
    return db_user

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
