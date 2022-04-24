from celery_app import app as celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task(name="send_notification", soft_time_limit=3600)
def send_notification(brand, discount, user):
    logger.info(
        "Simulating a email being sent because someone fetch the discount code."
    )
    return f"Sent Email to {brand} because {user} fetch the {discount} discount"


@celery.task(name="example_task", soft_time_limit=3600)
def example_task():
    logger.info("Test")
    return f"Test"
