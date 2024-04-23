from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()

engine = create_engine('postgresql://root:password@localhost:5466/testdb', echo=True)
    
class User(Base):
    __tablename__ = 'user'
    user_id = Column(String, primary_key=True)
    username = Column(String, nullable=True)
    first_name = Column(String)
    last_name = Column(String)

    def __repr__(self) -> str:
        return f"Username {self.username}"

# Initialize the database tables
# Base.metadata.create_all(engine)

session=scoped_session(sessionmaker(bind=engine))