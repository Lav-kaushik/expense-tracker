from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

# build mysql connection url
USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASSWORD")
DB = os.getenv("DB_NAME")
PORT = os.getenv("DB_PORT")
HOST = os.getenv("DB_HOST")

DATABASE_URL = f"mysql+pymysql://{USER}:{PASS}@{HOST}:{PORT}/{DB}"

# create engine
# echo = true is helpful for debugging to see raw sql queried
engine = create_engine(DATABASE_URL , echo=True)

# Create sessionLocal
# this will be used by the dependency to create actual database session
SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)

# Base class
# all the sqlalchemy models will inherit from this
Base = declarative_base()

def get_db():
    """Provide a database session to a FastAPI route."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

