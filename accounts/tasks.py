from celery import shared_task
from celery.utils.log import logger


@shared_task(name="send_email_async")
def send_email_async(msg):
    msg.send()
    logger.info("Email sent")
