from celery import shared_task

import logging
import redis

from .models import PostAnalytics, Post
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


@shared_task
def increment_post_views_task(slug, ip_address):
    try:
        post = Post.objects.get(slug=slug)
        post_analytics = PostAnalytics.objects.get(post=post)
        post_analytics.increment_view(ip_address)
    except Exception as e:
        logger.info(f"Error incrementing views for past slug {slug}: {str(e)}")


# TAREA que sincroniza las impresiones almacenadas en DB-Redis con la BD propia del sistema 
# y se ejecuta desde Celery-Beat

@shared_task
def sync_impressions_to_db():   
    # Recuperamos todos los post almacenados en DB-Redis
    keys = redis_client.keys("post:impressions:*")
    for key in keys:
        try:
            post_id = key.decode("utf-8").split(":")[-1]
            impressions = int(redis_client.get(key))
            
            #   Se reemplaza el atributo "created" por el guion bajo("_") ya no se usa este atributo
            analytics, _ = PostAnalytics.objects.get_or_create(post__id=post_id)
            analytics.impressions += impressions
            #   Se almacena a nivel BD esta impresion
            analytics.save()
            
            #   Se ejecuta el metodo "increment_impressions", el cual incrementa el numero de impresiones 
            #   y este valor lo registra en la BD
            analytics.increment_impressions()
            
            # Una vez que se ejecuta la tarea en un determinado post, lo eliminamos Redis
            redis_client.delete(key)
        except Exception as e:
            print(f"Error syncing impressions for {key}: {str(e)}")
            