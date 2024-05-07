from django.db import models

from django.db import models
from django.contrib.auth.models import User



class ConnectAPI(models.Model):
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
    parent_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connected_users', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s {self.broker} API Connection"
    
    
class StudentUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    linked_users = models.ManyToManyField(User, related_name='linked_student_users')

    def __str__(self):
        return f"StudentUser: {self.user.username}"
    

    
    