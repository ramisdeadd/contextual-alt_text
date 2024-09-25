
from typing import Annotated
from fastapi import Depends, Form, status, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import timedelta
from sqlmodel import Session
from database import engine
from auth.models import UserCreate, UserUpdate
from auth.router import router
from auth.schemas import User
from auth.dependencies import (
    get_current_active_user, 
    get_current_user, 
    get_password_hash, 
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

@router.post("/signup", response_class=HTMLResponse)
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



@router.post("/profile/update-profile", response_class=HTMLResponse)
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


async def create_user(user: Annotated[UserCreate, Depends(signup_user)]):
    with Session(engine) as session:
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    print(f"Succesful Signup")
    return db_user

async def update_user_profile(user: Annotated[UserUpdate, Depends(update_user)], 
                              curr_user: Annotated[User, Depends(get_current_active_user)]):
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