from sqlalchemy import Integer , Boolean , DateTime , String , Column , Float , ForeignKey
from database import Base
from datetime import datetime , timezone

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer , primary_key=True , unique=True)
    user_id = Column(Integer , ForeignKey("users.id") , nullable=False)
    item_name = Column(String(255) , index=True , nullable=False)
    amount = Column(Float , nullable=False)
    category = Column(String(255) , index=True , nullable=False)
    date = Column(DateTime(timezone=True) , nullable=False)
    created_at = Column(DateTime(timezone=True) , default=lambda : datetime.now(timezone.utc))