from sqlalchemy import UniqueConstraint, Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False) #Compulsory
    hashed_password = Column(String, nullable=False) #Compulsory
    created_timestamp = Column(DateTime, server_default=func.now())
    queries = relationship("Query", backref="owner")
    tags = relationship("Tag",backref="owner")

class Query(Base):
    __tablename__ = "query"
    id = Column(Integer, primary_key=True, index=True)
    query_name = Column(String, unique=True, nullable=False)
    query = Column(Text, nullable=False)
    report_type = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey("user_data.id"),nullable=False)
    create_timestamp = Column(DateTime, server_default=func.now())
    update_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now())
    tags = relationship("Tag", secondary="query_tag_mapping", backref="queries")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key = True, index=True)
    name = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey("user_data.id"),nullable=False)

    __table_args__ = (UniqueConstraint('name','created_by', name = 'unique_tag_per_user'),)

class QueryTag(Base):
    __tablename__ = "query_tag_mapping"
    query_id = Column(Integer, ForeignKey("query.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)