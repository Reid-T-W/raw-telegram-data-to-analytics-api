from sqlalchemy import Column, Integer, String, DateTime, Boolean, DECIMAL, ForeignKey, Enum as SQLAEnum, func, Float
from sqlalchemy.ext.declarative import declarative_base
from api.conn_db import Base_Analytics_Datastore
from sqlalchemy import Column, Integer, BigInteger, String, Boolean
from sqlalchemy.orm import relationship
class FactMessage(Base_Analytics_Datastore):
    __tablename__ = "fact_messages"
    __table_args__ = {"schema": "public_mart"}

    id = Column(Integer, primary_key=True, unique=True)
    # channel_dim_id = Column(BigInteger, nullable=True)
    channel_dim_id = Column(Integer, ForeignKey('dim_channels.id'))
    message_id = Column(String(255), nullable=True)
    message_text = Column(String(5000), nullable=True)
    date_dim_id = Column(BigInteger, nullable=True)
    llm_message_id = Column(String(255), nullable=True)
    intent = Column(String(255), nullable=True)
    product_name = Column(String(5000), nullable=True)
    has_image = Column(Boolean, nullable=True)

    channel = relationship('DimChannels', back_populates='messages')


class DimDate(Base_Analytics_Datastore):
    __tablename__ = "dim_dates"
    __table_args__ = {"schema": "public_mart"}

    id = Column(BigInteger, primary_key=True, unique=True)
    day = Column(Float, nullable=True)
    month = Column(Float, nullable=True)
    year = Column(Float, nullable=True)

class DimChannels(Base_Analytics_Datastore):
    __tablename__ = "dim_channels"
    __table_args__ = {"schema": "public_mart"}

    id = Column(BigInteger, primary_key=True, unique=True)
    channel_name = Column(String(255), nullable=True)

    messages = relationship('FactMessage', back_populates='channel', foreign_keys='FactMessage.channel_dim_id')

class FctImageDetection(Base_Analytics_Datastore):
    __tablename__ = "fct_image_detections"
    __table_args__ = {"schema": "public_mart"}

    id = Column(Integer, primary_key=True, unique=True)
    channel_name = Column(String(255), nullable=True)
    message_id = Column(String(255), nullable=True)
    item = Column(String(255), nullable=True)

class AggTopProducts(Base_Analytics_Datastore):
    __tablename__ = "agg_top_products"
    __table_args__ = {"schema": "public_mart"}

    product_name = Column(String(5000), primary_key=True, unique=True)
    count = Column(BigInteger, nullable=True)

