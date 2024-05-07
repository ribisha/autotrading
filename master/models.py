from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator

class StaffProfile(models.Model):
    user_staff = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_profile_image = models.ImageField(upload_to='Staff_images/', default='images/Angel_ONe.png', null=True)
    def save(self, *args, **kwargs):
        if not self.user_staff.password.startswith('pbkdf2_sha256$'):
            self.user_staff.password = make_password(self.user_staff.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.user_staff.username
 
class ClientProfile(models.Model):
    user_client = models.OneToOneField(User, on_delete=models.CASCADE)
    client_profile_image = models.ImageField(upload_to='client_images/', default='images/Angel_ONe.png', null=True)
    def save(self, *args, **kwargs):
        if not self.user_client.password.startswith('pbkdf2_sha256$'):
            self.user_client.password = make_password(self.user_client.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.user_client.username

class FinanceProfile(models.Model):
    user_finance = models.OneToOneField(User, on_delete=models.CASCADE)
    finance_profile_image = models.ImageField(upload_to='finance_images/', default='images/Angel_ONe.png', null=True)
    def save(self, *args, **kwargs):
        if not self.user_finance.password.startswith('pbkdf2_sha256$'):
            self.user_finance.password = make_password(self.user_finance.password)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.user_finance.username
    


class MasterClientadd(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
        return f"Masterclientadd: {self.user.username}"


class MasterConnectAPI(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    m_broker = models.CharField(max_length=50)
    m_api_key = models.CharField(max_length=100, null=True, blank=True)
    m_client_id = models.CharField(max_length=100)
    m_pin = models.CharField(max_length=10)
    m_qr_value=models.CharField(max_length=100)
    auth_token = models.CharField(max_length=255)
    m_fetched_data = models.JSONField(null=True, blank=True)
    m_balance_data = models.JSONField(null=True, blank=True)
    m_trade_data = models.JSONField(null=True, blank=True)
    m_option_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s {self.m_broker} API Connection"
    
    

class CreateRoom(models.Model):
    master_room = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.master_room.username