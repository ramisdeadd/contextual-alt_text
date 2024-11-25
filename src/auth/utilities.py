from auth.dependencies import get_user, get_password_hash
from auth.models import UserCreate
from auth.schemas import User
from sqlmodel import Session
from database import SessionDep

async def create_admin_user(session: SessionDep):
    exist_ok = await get_user("admin_user", session)
    
    if exist_ok is None:
        user = UserCreate(
            username = "admin_user",
            first_name = "admin_josh",
            last_name = "admin_lego",
            email = "admin@gmail.com",
            hashed_password = get_password_hash("1Adminsecret"),
            disabled = False,
            role = "admin",)
                   
        db_user = User.model_validate(user)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)