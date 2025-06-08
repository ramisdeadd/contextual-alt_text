from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL
from fastapi import Depends
from sqlmodel import SQLModel

url_object = URL.create(
    "postgresql+asyncpg",
    username='alttext_generator',
    password='KhU@%SLCkYOJt0',
    host="localhost",
    port=5432,
    database="alttext_generator_db"
)

engine = create_async_engine(url_object, echo=True)

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