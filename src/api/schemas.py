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

class AggTopProductsSchema(BaseModel):
    product_name: str
    count: int

class MessageAnalyticsSchema(BaseModel):
    total_no_of_messages: int
    messages_per_channel: dict

class MessageWithImagesAnalyticsSchema(BaseModel):
    total_no_of_messages_with_images: int
    messages_with_images_per_channel: dict

class MessageAnalyticsDayAggregateSchema(BaseModel):
    day: float
    month: float
    year: float
    count: int
class MessageAnalyticsMonthlyAggregateSchema(BaseModel):
    month: float
    year: float
    count: int
class MessageAnalyticsYearlyAggregateSchema(BaseModel):
    year: float
    count: int

class IntentAnalyticsSchema(BaseModel):
    intent: str
    count: int

class IntentAnalyticsPerChannelSchema(BaseModel):
    channel_name: str
    summary: list[IntentAnalyticsSchema]