from api import crud
from sqlalchemy.orm import Session

class AnalyticsService:
    
    @staticmethod
    def get_all_messages_service(session: Session):
        return crud.AnalyticsCrud.get_all_messages_crud(session)