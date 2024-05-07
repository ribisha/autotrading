from celery import shared_task, Celery
from master.utils import m_fetch_option_data
from client.models import ConnectAPI
from master.models import MasterConnectAPI
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from logzero import logger



from celery import Celery, shared_task
from .utils import m_fetch_option_data, m_fetch_balance_data
from .models import MasterConnectAPI
import logging

logger = logging.getLogger(__name__)


app = Celery('master')

@shared_task(bind=True, base=app.Task)
def update_data_periodically(self):
    try:
        # Fetch the first record from MasterConnectAPI
        master_instance = MasterConnectAPI.objects.first()
        if master_instance:
            m_api_key = master_instance.m_api_key
            m_client_id = master_instance.m_client_id
            m_pin = master_instance.m_pin
            m_qr_value = master_instance.m_qr_value

            # Fetch option data
            m_option_data = m_fetch_option_data(m_api_key, m_client_id, m_pin, m_qr_value)
            if m_option_data:
                # Update MasterConnectAPI
                master_instance.m_option_data = m_option_data
                master_instance.save()

                # Print the updated data
                logger.info(f"Data updated successfully: {m_option_data}")
            else:
                logger.error("Failed to fetch option data.")
        else:
            logger.error("No records found in MasterConnectAPI.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


def create_or_update_periodic_task(m_api_key, m_client_id, m_pin, m_qr_value):
    if not PeriodicTask.objects.filter(name='update_data_periodically_task').exists():
        interval_schedule, _ = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.MINUTES)
        task_args = [m_api_key, m_client_id, m_pin, m_qr_value]
        PeriodicTask.objects.create(
            interval=interval_schedule,
            name='update_data_periodically_task',
            task='master.tasks.update_data_periodically',
            args=task_args,
        )


