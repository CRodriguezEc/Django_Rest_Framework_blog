from celery import shared_task

import logging
import redis

from .models import PostAnalytics
from django.conf import settings

logger = logging.getLogger(__name__)

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)

@shared_task
def increment_post_impressions(post_id):
    #   Incrementa las impresiones del post asociado
    try:
        analytics, created = PostAnalytics.objects.get_or_create( post_id )
        analytics.increment_impressions()
    except Exception as e:
        logger.info(f"Error incrementing impressions for PostId {post_id}: {str(e)}")

# TAREA que sincroniza las impresiones almacenadas en DB-Redis con la BD propia del sistema        
@shared_task
def sync_impressions_to_db():   
    # Recuperamos todos los post almacenados en DB-Redis
    keys = redis_client.keys("post:impressions:*")
    for key in keys:
        try:
            post_id = key.decode("utf-8").split(":")[-1]
            impressions = int(redis_client.get(key))
            
            analytics, created = PostAnalytics.objects.get_or_create(post__id=post_id)
            analytics.impressions += impressions
            analytics.save()
            
            # Una vez que se ejecuta la tarea en un determinado post, lo eliminamos Redis
            redis_client.delete(key)
        except Exception as e:
            print(f"Error syncing impressions for {key}: {str(e)}")
            