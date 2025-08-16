

from sqlalchemy.orm import Session, aliased
from sqlalchemy import func
from api import models
from api import schemas


class AnalyticsCrud:

    @staticmethod
    def get_all_messages_crud(session: Session):
        return session.query(models.FactMessage).all()
    
    @staticmethod
    def get_top_products(session: Session, limit: int):
        return session.query(models.AggTopProducts).order_by(models.AggTopProducts.count.desc()).limit(limit).all()

    @staticmethod
    def get_message_analytics(session: Session):

        count = session.query(models.FactMessage).count()

        dc = aliased(models.DimChannels)
        count_by_channel = session.query(
                                    models.FactMessage.channel_dim_id, 
                                    models.DimChannels.channel_name,
                                    func.count(models.FactMessage.message_id).label('message_count')
                                ).join(models.DimChannels, models.DimChannels.id==models.FactMessage.channel_dim_id) \
                                    .group_by(models.FactMessage.channel_dim_id, models.DimChannels.channel_name)
                                    

        # Prepare payload
        messages_per_channel = {}
        for data in count_by_channel:
            messages_per_channel[data[1]] = data[2]

        message_analytics = schemas.MessageAnalyticsSchema(
            total_no_of_messages=count,
            messages_per_channel=messages_per_channel
        )

        return message_analytics
