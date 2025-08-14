from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from api import service
from api.conn_db import get_analytics_datastore_db
from api.schemas import FactMessageSchema

router = APIRouter()

@router.get("/messages", response_model = list[FactMessageSchema])
def get_messages(session: Session = Depends(get_analytics_datastore_db)):
    return service.AnalyticsService.get_all_messages_service(session)