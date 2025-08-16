from api import crud
from sqlalchemy.orm import Session

class AnalyticsService:
    
    @staticmethod
    def get_all_messages_service(session: Session):
        return crud.AnalyticsCrud.get_all_messages_crud(session)
    
    @staticmethod
    def get_top_products(session: Session, limit: int):
        return crud.AnalyticsCrud.get_top_products(session, limit)
    
    @staticmethod
    def get_message_analytics(session: Session):
        return crud.AnalyticsCrud.get_message_analytics(session)