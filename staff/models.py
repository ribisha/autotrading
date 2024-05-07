from django.db import models
from django.contrib.auth.models import User


class StaffConnectAPI(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    s_broker = models.CharField(max_length=50)
    s_api_key = models.CharField(max_length=100, null=True, blank=True)
    s_client_id = models.CharField(max_length=100)
    s_pin = models.CharField(max_length=10)
    s_qr_value=models.CharField(max_length=100)
    auth_token = models.CharField(max_length=255)
    s_fetched_data = models.JSONField(null=True, blank=True)
    s_balance_data = models.JSONField(null=True, blank=True)
    s_trade_data = models.JSONField(null=True, blank=True)
    s_option_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s {self.s_broker} API Connection"



class StaffClientAdd(models.Model):
    s_client_user = models.OneToOneField(User, on_delete=models.CASCADE)
    broker = models.CharField(max_length=50)
    api_key = models.CharField(max_length=100, null=True, blank=True)
    client_id = models.CharField(max_length=100)
    pin=models.CharField(max_length=10)
    qr_value=models.CharField(max_length=100)
    auth_token = models.CharField(max_length=255)
    fetched_data = models.JSONField(null=True, blank=True)
    balance_data = models.JSONField(null=True, blank=True)
    trade_data = models.JSONField(null=True, blank=True)
    option_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"StaffClientAdd: {self.s_client_user.username}"
