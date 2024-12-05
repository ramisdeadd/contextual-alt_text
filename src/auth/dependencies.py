from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException, status, Cookie
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select, SQLModel
from typing import TypeVar
from sqlalchemy.sql import func
from sqlmodel.sql.expression import SelectOfScalar
from database import SessionDep
from auth.models import UserCreate, UserPasswordUpdate, UserUpdate
from auth.schemas import User, PaginationInput, UserPage, AltCapPage
from post.schemas import Image, AltText
import jwt
import re
import uuid

T = TypeVar("T", bound=SQLModel)

SECRET_KEY = "aafb48d530ee71c753e64e6830439b026c9405685c19b8829b8065c881ad2876"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)

async def get_user(username: str, session: SessionDep) -> User:
    statement = select(User).where(User.username == username)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    return user

async def authenticate_user(username: str, plain_password: str, session: SessionDep):
    user = await get_user(username, session)
    if not user:
        return False
    if user.disabled:
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

async def get_current_user(session: SessionDep,
                           token: Annotated[str, Cookie(...)] = None,
                           allow: bool = None,
                           ):
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
    user = await get_user(username=username, session=session)
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
        curr_user: Annotated[User, Depends(get_current_active_user)],
        session: SessionDep
) -> User:
    valid_user = UserPasswordUpdate.model_validate(user)

    curr_user.hashed_password = valid_user.hashed_password

    session.add(curr_user)
    await session.commit()
    await session.refresh(curr_user)

    return curr_user

async def create_user(user: UserCreate, session: SessionDep) -> User:
    db_user = User.model_validate(user)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

async def check_user_exist(user: UserCreate, session: SessionDep):
    username_statement = select(User).where(User.username == user.username)
    username_result = await session.execute(username_statement)
    existing_user = username_result.scalar_one_or_none()

    email_statement = select(User).where(User.email == user.email)
    email_result = await session.execute(email_statement)
    existing_email = email_result.scalar_one_or_none()

    if existing_user or existing_email:
        return False
    else:
        return True

async def update_user_username(user: UserUpdate,
                               curr_user: User,
                               session: SessionDep) -> User:
    valid_user = UserUpdate.model_validate(user)

    curr_user.username = valid_user.username
    
    session.add(curr_user)
    await session.commit()
    await session.refresh(curr_user)
    
    return curr_user

async def update_user_profile(user: UserUpdate, 
                              curr_user: User,
                              session: SessionDep) -> User:
    valid_user = UserUpdate.model_validate(user)
            
    curr_user.first_name = valid_user.first_name
    curr_user.last_name = valid_user.last_name
    curr_user.email = valid_user.email
    curr_user.disabled = valid_user.disabled

    session.add(curr_user)
    await session.commit()
    await session.refresh(curr_user)
    
    return curr_user


async def get_all_users(session: SessionDep):
    statement = select(User).where(User.role == 'user')
    result = await session.execute(statement)
    users = result.all()
    return users
    
def verify_username(username):
    regex = r"[^a-zA-Z0-9]"

    if len(username) < 6 or len(username) > 13:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error - username length",
        )

    if re.search(regex, username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error - username regex",
        )

def verify_first_name(first_name):
    regex = r"^[a-zA-Z ]+$"

    # Check for white space leading or trailing
    if first_name != first_name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error - last name has training / leading spaces",
        )

    # Check length
    if len(first_name) < 2 or len(first_name) > 40:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error - first name length",
        )
    
    # Check for last name regex
    if not re.fullmatch(regex, first_name):
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error - first name regex",
        )
    
def verify_last_name(last_name):
    regex = r"^[a-zA-Z]+$"

    # Check for white space leading or trailing
    if last_name != last_name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error - last name has training / leading spaces",
        )
    
    # Check length
    if len(last_name) < 2 or len(last_name) > 40:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error - last name  length",
        )
    
    # Check for last name regex
    if not re.fullmatch(regex, last_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error - last name regex",
        )

def verify_email(email: str):
    email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

    # Check for email regex
    if not re.fullmatch(email_pattern, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error - invalid email format",
        )
    
def verify_password_strength(password: str):
    # Check length
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long",
        )
    
    # Check for at least one number
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one number",
        )
    
    # Check for at least one uppercase character
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one uppercase character",
        )
    
    # Check for at least one lowercase character
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one lowercase character",
        )
    
    # Check for spaces
    if re.search(r"\s", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must not contain spaces",
        )

async def get_user_generated_history(curr_user: User, session: SessionDep):
    statement = select(Image).where(Image.user_id == curr_user.id)
    result = await session.execute(statement)
    history = result.all()
    history = [image for (image,) in history]
    return history

async def get_image_alt_text(curr_image: Image, session: SessionDep):
    statement = select(AltText).where(AltText.image_id == curr_image.id)
    result = await session.execute(statement)
    history = result.one()
    return history[0]

async def disable_image_alt(curr_user: User, image_id: str, session: SessionDep):
    try:
        image_uuid = uuid.UUID(image_id)  # Convert the string to a UUID
    except ValueError:
        print(f"Invalid UUID: {image_id}")
        return

    image_statement = select(Image).where(Image.id == image_uuid)
    image_result = await session.execute(image_statement)
    image = image_result.scalar_one_or_none()

    if image:
        image.disabled = True
        session.add(image)
        await session.commit()
        await session.refresh(image)
        print(f"IMAGE DISABLED: {image}")
    else:
        print(f"IMAGE NOT FOUND: {image_id}")

async def disable_user_acc(user_id : str, session: SessionDep):
    try:
        user_uuid = uuid.UUID(user_id)  # Convert the string to a UUID
    except ValueError:
        print(f"Invalid UUID: {user_id}")
        return

    user_statement = select(User).where(User.id == user_uuid)
    user_result = await session.execute(user_statement)
    user = user_result.scalar_one_or_none()

    if user:
        user.disabled = True
        session.add(user)
        await session.commit()
        await session.refresh(user)
    else:
        print(f"USER NOT FOUND: {user_id}")
    
async def altcap_paginate (
        image_query: SelectOfScalar[T],
        alt_query: SelectOfScalar[T],
        session: SessionDep,
        pagination_input: PaginationInput
) -> AltCapPage[T]:
    # Turn original query into subquery
    subquery = image_query.subquery()

    # Another select statement that counts the rows in the subquery
    # Merges the subquery and this query into one and ready for execution
    count_statement = select((func.count())).select_from(subquery)

    # count_statement is now the entire full statement
    # Execute counte_statement get the scalar result (total number of items)
    # Returns a single integer
    total_items = await session.scalar(count_statement)
    assert isinstance(total_items, int)

    # Out-of-bounds requests goes directly to last page
    # Ex: (151 + 50) // 50 = 4
    # The last extra item is placed alone on 4 due to //
    total_pages = (total_items + pagination_input.page_size - 1) // pagination_input.page_size

    # Gives at least 1 page even if no items exist from search
    # max function returns either total_pages or at least 1
    total_pages = max(total_pages, 1)

    # min function returns either page or total pages
    # If user enteres a pagination_input.page higher than total pages (out-of-bounds)
    # will automatically return the highest numbered page
    current_page = min(pagination_input.page, total_pages)

    # Decides when the number of items start showing. Offset of the starting point
    # of the items retrieved. Ex: (2 - 1) * 50 | Page 2 will start showing items
    # starting from item 50
    offset = (current_page - 1) * pagination_input.page_size

    # Gets the selected number of items to be displayed on the page. Starts from offset
    # and is limited to the number of items can be displayed on the page (page_size)
    image_result = await session.execute(image_query.offset(offset).limit(pagination_input.page_size))
    alt_result = await session.execute(alt_query.offset(offset).limit(pagination_input.page_size))

    # Turns all the items from the result into a list 
    images = image_result.all()
    images = [item for i in images for item in i]

    alttext = alt_result.all()
    alttext = [item for a in alttext for item in a]

    # No idea
    start_index = offset + 1 if total_items > 0 else 0
    end_index = min(offset + pagination_input.page_size, total_items)

    return AltCapPage[T](
        images=images,
        alttext=alttext,
        total_items=total_items,
        start_index=start_index,
        end_index=end_index,
        total_pages=total_pages,
        current_page_size=len(images),  # can differ from the requested page_size
        current_page=current_page,  # can differ from the requested page
    )

async def user_paginate (
        query: SelectOfScalar[T],
        session: SessionDep,
        pagination_input: PaginationInput
) -> UserPage[T]:
    subquery = query.subquery()

    count_statement = select((func.count())).select_from(subquery)

    total_items = await session.scalar(count_statement)
    assert isinstance(total_items, int)

    total_pages = (total_items + pagination_input.page_size - 1) // pagination_input.page_size

    total_pages = max(total_pages, 1)
    current_page = min(pagination_input.page, total_pages)

    offset = (current_page - 1) * pagination_input.page_size

    result = await session.execute(query.offset(offset).limit(pagination_input.page_size))

    users = list(result.scalars().all())

    start_index = offset + 1 if total_items > 0 else 0
    end_index = min(offset + pagination_input.page_size, total_items)

    return UserPage[T](
        users=users,
        total_items=total_items,
        start_index=start_index,
        end_index=end_index,
        total_pages=total_pages,
        current_page_size=len(users),  # can differ from the requested page_size
        current_page=current_page,  # can differ from the requested page
    )

PaginationDep = Annotated[PaginationInput, Depends()]
CurrUserDep = Annotated[User, Depends(get_current_active_user)]