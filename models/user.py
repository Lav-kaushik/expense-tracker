from sqlalchemy import Integer , Boolean , DateTime , String , Column , Float , ForeignKey
from database import Base
from datetime import datetime , timezone

class User(Base):
    __tablename__ = "users"
    # It tells the database to create an index on that column.
    # An index is a data structure (like a sorted lookup table) that makes search faster.
    id = Column(Integer , primary_key=True , index=True)
    username = Column(String(50) , unique=True , index=True , nullable=False)
    email = Column(String(30) , unique=True , index=True , nullable=False)
    hashed_password = Column(String(255) , nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True) , default=lambda : datetime.now(timezone.utc))