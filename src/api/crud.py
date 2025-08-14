

from sqlalchemy.orm import Session
from api import models


class AnalyticsCrud:

    @staticmethod
    def get_all_messages_crud(session: Session):
        return session.query(models.FactMessage).all()