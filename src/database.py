from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlmodel import SQLModel
postgres_file_name = "alt_text_db"
postgres_url = f"postgresql+asyncpg://myuser:myuser-fastapi@localhost/{postgres_file_name}"

engine = create_async_engine(postgres_url, echo=True)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
    
SessionDep = Annotated[AsyncSession, Depends(get_session)]