from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException, status, Cookie
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from database import engine
from auth.models import UserCreate, UserPasswordUpdate, UserUpdate
from auth.schemas import User
from post.schemas import Image, AltText
import jwt

SECRET_KEY = "aafb48d530ee71c753e64e6830439b026c9405685c19b8829b8065c881ad2876"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

async def create_user(user: UserCreate):
    with Session(engine) as session:
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    print(f"Succesful Signup")
    return db_user

async def update_user_profile(user: UserUpdate, 
                              curr_user: User):
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

def get_user_generated_history(curr_user: User):
    with Session(engine) as session:
        statement = select(Image).where(Image.user_id == curr_user.id)
        result = session.exec(statement)
        history = result.all()
    return history

def get_image_alt_text(curr_image: Image):
    with Session(engine) as session:
        statement = select(AltText).where(AltText.image_id == curr_image.id)
        result = session.exec(statement)
        history = result.one()
    return history
