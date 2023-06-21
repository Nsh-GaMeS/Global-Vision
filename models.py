# specify the columns in the database in the users database. includes two tabels Users tabel and ResourceUrl table

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class ResourceUrl(Base):
    __tablename__ = "resourceurl"

    id = Column(Integer, primary_key=True, index=True)
    url_with_query_string = Column(String)
