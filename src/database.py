from sqlmodel import SQLModel, create_engine

sqlite_file_name = "alt-text.db"
sqlite_url = f"sqlite:///../data/{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

