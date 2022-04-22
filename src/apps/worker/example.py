from celery_app import app as celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task(name="example_task", soft_time_limit=3600)
def example_task():
    logger.info("The sample task just ran.")
    return f"Example task runned"
