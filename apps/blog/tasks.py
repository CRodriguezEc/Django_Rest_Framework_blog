from celery import shared_task

import logging

from .models import PostAnalytics

logger = logging.getLogger(__name__)

@shared_task
def increment_post_impressions(post_id):
    #   Incrementa las impresiones del post asociado
    try:
        analytics, created = PostAnalytics.objects.get_or_create( post_id )
        analytics.increment_impressions()
    except Exception as e:
        logger.info(f"Error incrementing impressions for PostId {post_id}: {str(e)}")
        