

from re import L
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

    @staticmethod
    def get_message_analytics_day_aggregate(session: Session):
        return session.query(models.AggMessagesDaily).all()

    @staticmethod
    def get_message_analytics_mothly_aggregate(session: Session):
        return session.query(models.AggMessagesMonthly).all()

    @staticmethod
    def get_message_analytics_yearly_aggregate(session: Session):
        return session.query(models.AggMessagesYearly).all()
    
    @staticmethod
    def get_message_image_analytics(session: Session):
        # Get Total no of messages with images
        total_no_of_messages_with_images = session.query(models.FctImageDetection).count()
        
        # Total no of messages with images in each channel
        count_by_channel = session.query(
                                            models.FctImageDetection.channel_name, 
                                            func.count(models.FctImageDetection.id).label('message_with_image_count')
                                        ).group_by(models.FctImageDetection.channel_name)
        
        # Prepare payload
        messages_with_images_per_channel = {}
        for data in count_by_channel:
            messages_with_images_per_channel[data[0]] = data[1]

        message_analytics = schemas.MessageWithImagesAnalyticsSchema(
            total_no_of_messages_with_images=total_no_of_messages_with_images,
            messages_with_images_per_channel=messages_with_images_per_channel
        )

        return message_analytics
    
    @staticmethod
    def get_intent_analytics(session: Session):
        intent_analytics = session.query(
                                            models.FactMessage.intent, 
                                            func.count(models.FactMessage.id).label('count')
                                        ).group_by(models.FactMessage.intent)
        return intent_analytics

    @staticmethod
    def get_intent_analytics_per_channel(session: Session):
        
        # Get all channels
        channels = session.query(
            models.DimChannels
        )

        # Iterate through the channels and get the intents per channel
        response = []
        for channel in channels:
            # Get intent summary
            intent_analytics_per_channel = session.query(
                                    models.FactMessage.intent,
                                    func.count(models.FactMessage.id).label('count')
                                ).filter(models.FactMessage.channel_dim_id==channel.id) \
                                .group_by(models.FactMessage.intent)
            
            per_channel_intent_summary = []

            for record in intent_analytics_per_channel:
                data = schemas.IntentAnalyticsSchema(
                    intent=record.intent,
                    count=record.count
                )

                per_channel_intent_summary.append(data)
            
            analytics_summary = schemas.IntentAnalyticsPerChannelSchema(
                channel_name = channel.channel_name,
                summary = per_channel_intent_summary
            )

            response.append(analytics_summary)
        return response