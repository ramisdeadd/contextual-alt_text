import os
import json
from datetime import datetime, timedelta, timezone
from typing import Union, Annotated

import jwt
import uvicorn
import hashlib
import PIL.Image
from pydantic import BaseModel
from pathlib import Path
from sqlmodel import Field, Session, SQLModel, create_engine, select, UniqueConstraint
from sqlalchemy import Column, Integer
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, UploadFile, File, Form, HTTPException, status, Cookie, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from generate import create_alttext

SECRET_KEY = "aafb48d530ee71c753e64e6830439b026c9405685c19b8829b8065c881ad2876"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

class UserBase(SQLModel):
    username: str = Field(index=True)
    first_name: str
    last_name: str
    email: str = Field(unique=True)
    disabled: bool = Field(default=False)

class UserUpdate(SQLModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    disabled: bool | None = None

class UserPasswordUpdate(UserUpdate):
    hashed_password: str | None = None

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    hashed_password: str

class UserPublic(UserBase):
    id: int

class ImageBase(SQLModel):  
    user_id: int | None = Field(default=None, foreign_key="user.id")
    caption: str 
    caption_edit: str | None = None

class Image(ImageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hash: str = Field(unique=True, )

    __table_args__ = (
        UniqueConstraint("user_id", "hash"),
    )

class AltTextBase(SQLModel):
    image_id: int | None = Field(default=None, foreign_key="image.id")
    generated_alt: str
    edited_alt: str | None = None

class AltText(AltTextBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Server ....")
    create_db_and_tables()
    create_admin_user()
    yield
    print("Stopping Server ....")

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

sqlite_file_name = "alt-text.db"
sqlite_url = f"sqlite:///../data/{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_admin_user():
    exist_ok = get_user("admin_user")
    
    if exist_ok is None:
        user = UserCreate(
            username = "admin_user",
            first_name = "admin_josh",
            last_name = "admin_lego",
            email = "admin@gmail.com",
            hashed_password = get_password_hash("1Adminsecret"),
            disabled = False,
)

        with Session(engine) as session:
            db_user = User.model_validate(user)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)

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
        expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Cookie(...)] = None, allow: bool = None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    credentials_timeout = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token Timeout",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Checks if user is authenticated and if endpoint allows non-authenticated users
    # Returns none to indicate to display non-authenticated endpoint
    if token == None and allow == True:
        return None
    
    if token == None:
        print("Token Error - Nonexistent")
        raise credentials_exception
    
    try:
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
    except InvalidTokenError:
        raise credentials_timeout
    
    print(f"Username: {username}")
    user = get_user(username=username)
    if user is None:
        print("Token Error - User Not Found")
        raise credentials_exception
    return user

async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):  
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    
    return current_user

# read_users_me -> get_current_active_user -> get_current_user -> get_user
@app.get("/profile", response_class=HTMLResponse)
async def read_users_me(request: Request, current_user: Annotated[str, Depends(get_current_active_user)]):
    return templates.TemplateResponse("/pages/profile.html", {"request": request, "user": current_user})

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, token: Annotated[str, Cookie(...)] = None):
    try:
        user = await get_current_user(token=token, allow=True)
        if user == None:
            return templates.TemplateResponse("/pages/index.html", {"request": request, "user": None})
        return templates.TemplateResponse("/pages/index.html", {"request": request, "user": user})
    except HTTPException as error: 
        if error.status_code == status.HTTP_401_UNAUTHORIZED:
            response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
            response.delete_cookie("token")
            return response
        raise error

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("/pages/login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("/pages/signup.html", {"request": request})

@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("token")
    return response

@app.post("/profile/update-profile", response_class=HTMLResponse)
async def update_user(
    username: Annotated[str, Form()],
    first_name: Annotated[str, Form()],
    last_name: Annotated[str, Form()], 
    email: Annotated[str, Form()], 
    token: Annotated[str, Cookie(...)],
    disabled: Annotated[bool, Form()] = 0,
):
    user = UserUpdate(
        username = username,
        first_name = first_name,
        last_name = last_name,
        email = email,
        disabled = disabled,
    )
    curr_user = await get_current_active_user(await get_current_user(token = token, allow = None))
    user = await update_user_profile(user, curr_user)
    print(f"Updated User {user.username}")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user.username}, 
        expires_delta = access_token_expires
    )

    print(f"access token {access_token}")

    response = RedirectResponse("/profile", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="token", value=f"Bearer {access_token}", httponly=True)
    return response

@app.post("/profile/change-password", response_class=HTMLResponse)
async def change_password(
    password: Annotated[str, Form()],
    # TO DO validate confirm_password
    confirm_password: Annotated[str, Form()],
    token: Annotated[str, Cookie(...)]
):
    
    hashed_password = get_password_hash(password)
    user = UserPasswordUpdate(
        hashed_password=hashed_password
    )

    curr_user = await get_current_active_user(await get_current_user(token = token, allow = None))
    user = await change_user_password(user, curr_user)

    response = RedirectResponse("/profile", status_code=status.HTTP_302_FOUND)
    return response

@app.post("/login", response_class=HTMLResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
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

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="token", value=f"Bearer {access_token}", httponly=True)

    return response

@app.post("/signup", response_class=HTMLResponse)
async def signup_user(username: Annotated[str, Form()],
                      first_name: Annotated[str, Form()],
                      last_name: Annotated[str, Form()], 
                      email: Annotated[str, Form()], 
                      plain_password: Annotated[str, Form()]):
    hashed_password = get_password_hash(plain_password)
    user = UserCreate(
        username = username,
        first_name = first_name,
        last_name = last_name,
        email = email,
        hashed_password = hashed_password,
        disabled = False,
    )
    user = await create_user(user)
    response = RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    return response 

async def create_user(user: Annotated[UserCreate, Depends(signup_user)]):
    with Session(engine) as session:
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    print(f"Succesful Signup")
    return db_user

async def update_user_profile(user: Annotated[UserUpdate, Depends(update_user)], curr_user: Annotated[User, Depends(get_current_active_user)]):
    with Session(engine) as session:
        valid_user = UserUpdate.model_validate(user)

        curr_user.username = valid_user.username
        curr_user.first_name = valid_user.first_name
        curr_user.last_name = valid_user.last_name
        curr_user.email = valid_user.email
        curr_user.disabled = valid_user.disabled

        session.add(curr_user)
        session.commit()
        session.refresh(curr_user)
    
    return curr_user

async def change_user_password(
        user: Annotated[UserPasswordUpdate, Depends()], 
        curr_user: Annotated[User, Depends(get_current_active_user)]
):
    with Session(engine) as session:
        valid_user = UserPasswordUpdate.model_validate(user)

        curr_user.hashed_password = valid_user.hashed_password

        session.add(curr_user)
        session.commit()
        session.refresh(curr_user)
        print("PASSWORD UPDATED")
    return curr_user

async def generate_image_hash(
        img_path: Path
):
        with open(img_path, "rb") as f:
            bytes = f.read()
            readable_hash = hashlib.md5(bytes).hexdigest()

        return readable_hash

@app.post("/")
async def generate_alt_text(
    text: Annotated[str, Form()], 
    token: Annotated[str, Cookie(...)] = None,
    img: UploadFile = File(...)
):
    print(img)
    size = (1920, 1080)

    user = await get_current_user(token=token, allow=True)
    if user == None:
        response = RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
        return response
    
    img_content = await img.read()
    img_path = Path(f"images/{img.filename}")
    with open(img_path, "wb") as f:
        f.write(img_content)

    with PIL.Image.open(img_path) as image:
        image.save(img_path, dpi=size)
        image_hash = await generate_image_hash(img_path)

    image_exist = await check_image_exist(user, image_hash)        
    generator_output = create_alttext(text, img_path, image_exist, vision_model="BLIP")
    
    image_db = await save_image_gen(user, image_hash, generator_output["image-caption"])
    alttext_db = await save_alt_gen(image_db, generator_output["alt-text"])

    # Remove image after use
    img_path.unlink()

    return JSONResponse(content={
        "generated-alt-text": generator_output["alt-text"],
        "generated-image-caption": generator_output["image-caption"],
    }) 

async def save_alt_gen(
        image: Annotated[Image, Depends(generate_alt_text)],
        generated_alt: str,
):
    with Session(engine) as session:
        alt_text = AltText(
            image_id = image.id,
            generated_alt = generated_alt,
        )

        session.add(alt_text)
        session.commit()
        session.refresh(alt_text)
    
    return alt_text

async def check_image_exist(
        user: Annotated[User, Depends(generate_alt_text)],
        image_hash: str
):
     with Session(engine) as session:
        # Check if image hash already exists
        statement = select(Image).where(
            Image.hash == image_hash,
            Image.user_id == user.id
        )
        results = session.exec(statement)
        image = results.first()

        # Returns already existing image
        if image is not None: 
            return image
        else:
            return None

async def save_image_gen(
        user: Annotated[User, Depends(generate_alt_text)],
        image_hash: str,
        caption: str,
):
    with Session(engine) as session:
        image = Image(
            caption = caption,
            hash = image_hash,
            user_id = user.id
        )

        session.add(image)
        session.commit()
        session.refresh(image)

    return image

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


