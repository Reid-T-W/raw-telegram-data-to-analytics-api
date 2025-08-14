from sqlalchemy import Column, Integer, String, DateTime, Boolean, DECIMAL, ForeignKey, Enum as SQLAEnum, func, Float
from sqlalchemy.ext.declarative import declarative_base
from api.conn_db import Base_Analytics_Datastore
from sqlalchemy import Column, Integer, BigInteger, String, Boolean

class FactMessage(Base_Analytics_Datastore):
    __tablename__ = "fact_messages"
    __table_args__ = {"schema": "public_mart"}

    id = Column(Integer, primary_key=True, nullable=True)  # int4
    channel_dim_id = Column(BigInteger, nullable=True)  # int8
    message_id = Column(String(255), nullable=True)  # varchar(255)
    message_text = Column(String(5000), nullable=True)  # varchar(5000)
    date_dim_id = Column(BigInteger, nullable=True)  # int8
    llm_message_id = Column(String(255), nullable=True)  # varchar(255)
    intent = Column(String(255), nullable=True)  # varchar(255)
    product_name = Column(String(5000), nullable=True)  # varchar(5000)
    has_image = Column(Boolean, nullable=True)  # bool

class DimDate(Base_Analytics_Datastore):
    __tablename__ = "dim_dates"
    __table_args__ = {"schema": "public_mart"}

    id = Column(BigInteger, primary_key=True, nullable=True)
    day = Column(Float, nullable=True)
    month = Column(Float, nullable=True)
    year = Column(Float, nullable=True)

class DimChannels(Base_Analytics_Datastore):
    __tablename__ = "dim_channels"
    __table_args__ = {"schema": "public_mart"}

    id = Column(BigInteger, primary_key=True, nullable=True)
    channel_name = Column(String(255), nullable=True)

class FctImageDetection(Base_Analytics_Datastore):
    __tablename__ = "fct_image_detections"
    __table_args__ = {"schema": "public_mart"}

    id = Column(Integer, primary_key=True, nullable=True)
    channel_name = Column(String(255), nullable=True)
    message_id = Column(String(255), nullable=True)
    item = Column(String(255), nullable=True)

