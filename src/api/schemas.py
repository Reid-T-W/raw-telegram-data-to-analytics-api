from pydantic import BaseModel
from datetime import datetime

class FactMessageSchema(BaseModel):
    id: int
    channel_dim_id: int
    message_id: int
    message_text: str
    date_dim_id: int
    llm_message_id: int
    intent: str
    product_name: str
    has_image: bool

class DimDateSchema(BaseModel):
    id: int
    day: int
    month: int
    year: int

class DimChannelSchema(BaseModel):
    id: int
    channel_name: str