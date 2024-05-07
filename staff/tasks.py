from celery import shared_task, Celery
from staff.utils import s_fetch_option_data
from staff.models import *
# from master.models import MasterConnectAPI
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from logzero import logger



from celery import Celery, shared_task
from .utils import s_fetch_option_data
from .models import StaffConnectAPI
import logging

logger = logging.getLogger(__name__)


app = Celery('staff')

@shared_task(bind=True, base=app.Task)
def update_data_periodically(self):
    try:
        # Fetch the first record from MasterConnectAPI
        staff_instance = StaffConnectAPI.objects.first()
        if staff_instance:
            s_api_key = staff_instance.s_api_key
            s_client_id = staff_instance.s_client_id
            s_pin = staff_instance.s_pin
            s_qr_value = staff_instance.s_qr_value

            # Fetch option data
            s_option_data = s_fetch_option_data(s_api_key, s_client_id, s_pin, s_qr_value)
            if s_option_data:
                # Update MasterConnectAPI
                staff_instance.s_option_data = s_option_data
                staff_instance.save()

                # Print the updated data
                logger.info(f"Data updated successfully: {s_option_data}")
            else:
                logger.error("Failed to fetch option data.")
        else:
            logger.error("No records found in MasterConnectAPI.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


def create_or_update_periodic_task(s_api_key, s_client_id, s_pin, s_qr_value):
    if not PeriodicTask.objects.filter(name='update_data_periodically_task').exists():
        interval_schedule, _ = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.MINUTES)
        task_args = [s_api_key, s_client_id, s_pin, s_qr_value]
        PeriodicTask.objects.create(
            interval=interval_schedule,
            name='update_data_periodically_task',
            task='staff.tasks.update_data_periodically',
            args=task_args,
        )


