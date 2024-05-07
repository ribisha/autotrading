from django.contrib.auth.models import User
from django.db import models


class MasterAccount(models.Model):
    user_master = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True, blank=True)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    district = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=255, blank=True)
    parent_name = models.CharField(max_length=255, blank=True)
    nominee_name = models.CharField(max_length=255, blank=True)
    nominee_relationship = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.full_name or str(self.user_master)
class ClientAccount(models.Model):
    user_client = models.OneToOneField(User, on_delete=models.CASCADE)
    client_full_name = models.CharField(max_length=255, blank=True)
    client_profile_image = models.ImageField(upload_to='client_profile_images/', null=True, blank=True)
    client_date_of_birth = models.DateField(null=True, blank=True)
    CLIENT_GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    client_gender = models.CharField(max_length=6, choices=CLIENT_GENDER_CHOICES, blank=True)
    client_phone = models.CharField(max_length=15, blank=True)
    client_email = models.EmailField(blank=True)
    client_address = models.TextField(blank=True)
    client_pincode = models.CharField(max_length=10, blank=True)
    client_district = models.CharField(max_length=255, blank=True)
    client_state = models.CharField(max_length=255, blank=True)
    client_occupation = models.CharField(max_length=255, blank=True)
    client_parent_name = models.CharField(max_length=255, blank=True)
    client_nominee_name = models.CharField(max_length=255, blank=True)
    client_nominee_relationship = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.client_full_name or str(self.user_client)
    
    
class Courses(models.Model):
    course_name = models.CharField(max_length=255)
    course_price = models.DecimalField(max_digits=10, decimal_places=2)
    course_image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    def __str__(self):
        return self.course_name
class SelectedCourses(models.Model):
    client_account = models.ForeignKey('ClientAccount', on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.client_account.user_client.username} - {self.course.course_name}"
class StaffAccount(models.Model):
    user_staff = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_full_name = models.CharField(max_length=255, blank=True)
    staff_profile_image = models.ImageField(upload_to='staff_profile_images/', null=True, blank=True)
    staff_date_of_birth = models.DateField(null=True, blank=True)
    STAFF_GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    staff_gender = models.CharField(max_length=6, choices=STAFF_GENDER_CHOICES, blank=True)
    staff_phone = models.CharField(max_length=15, blank=True)
    staff_email = models.EmailField(blank=True)
    staff_address = models.TextField(blank=True)
    staff_pincode = models.CharField(max_length=10, blank=True)
    staff_district = models.CharField(max_length=255, blank=True)
    staff_state = models.CharField(max_length=255, blank=True)
    staff_occupation = models.CharField(max_length=255, blank=True)
    staff_parent_name = models.CharField(max_length=255, blank=True)
    staff_nominee_name = models.CharField(max_length=255, blank=True)
    staff_nominee_relationship = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.staff_full_name or str(self.user_staff)
class FinanceAccount(models.Model):
    user_finance = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user_finance