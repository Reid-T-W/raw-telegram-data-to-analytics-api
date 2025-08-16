from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from api import service
from api.conn_db import get_analytics_datastore_db
from api.schemas import AggTopProductsSchema, FactMessageSchema, IntentAnalyticsPerChannelSchema, IntentAnalyticsSchema, MessageAnalyticsDayAggregateSchema, MessageAnalyticsMonthlyAggregateSchema, MessageAnalyticsSchema, MessageAnalyticsYearlyAggregateSchema, MessageWithImagesAnalyticsSchema

router = APIRouter()

@router.get("/messages", response_model = list[FactMessageSchema])
def get_messages(
    session: Session = Depends(get_analytics_datastore_db)
):
    return service.AnalyticsService.get_all_messages_service(session)

@router.get("/top_proudcts", response_model = list[AggTopProductsSchema])
def get_top_products(
    limit: int,
    session: Session = Depends(get_analytics_datastore_db)
):
    return service.AnalyticsService.get_top_products(session, limit)

@router.get("/message-analytics", response_model = MessageAnalyticsSchema)
def get_message_analytics(
    session: Session = Depends(get_analytics_datastore_db)
):
    return service.AnalyticsService.get_message_analytics(session)

@router.get("/message-analytics/day-aggregate", response_model = list[MessageAnalyticsDayAggregateSchema])
def get_message_analytics_day_aggregate(
    session: Session = Depends(get_analytics_datastore_db)
):
    return service.AnalyticsService.get_message_analytics_day_aggregate(session)

@router.get("/message-analytics/month-aggregate", response_model = list[MessageAnalyticsMonthlyAggregateSchema])
def get_message_analytics_mothly_aggregate(
    session: Session = Depends(get_analytics_datastore_db)
):
    return service.AnalyticsService.get_message_analytics_mothly_aggregate(session)

@router.get("/message-analytics/year-aggregate", response_model = list[MessageAnalyticsYearlyAggregateSchema])
def get_message_analytics_yearly_aggregate(
    session: Session = Depends(get_analytics_datastore_db)
):
    return service.AnalyticsService.get_message_analytics_yearly_aggregate(session)

@router.get("/message-image-analytics", response_model = MessageWithImagesAnalyticsSchema)
def get_message_image_analytics(
    session: Session = Depends(get_analytics_datastore_db)
):
    return service.AnalyticsService.get_message_image_analytics(session)

@router.get("/intent-analytics", response_model = list[IntentAnalyticsSchema])
def get_intent_analytics(
    session: Session = Depends(get_analytics_datastore_db)
):
    return service.AnalyticsService.get_intent_analytics(session)

@router.get("/intent-analytics/per_channel", response_model = list[IntentAnalyticsPerChannelSchema])
def get_intent_analytics_per_channel(
    session: Session = Depends(get_analytics_datastore_db)
):
    return service.AnalyticsService.get_intent_analytics_per_channel(session)
