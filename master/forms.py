from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import StaffProfile
from authentication . models import *



class MasterAccountForm(forms.ModelForm):
    class Meta:
        model = MasterAccount
        fields = '__all__'







class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = '__all__'
    def clean_user(self):
        user = self.cleaned_data.get('user')
        if not user.password.startswith('pbkdf2_sha256$'):
            user.password = make_password(user.password)
        return user
    def save(self, commit=True):
        instance = super().save(commit=False)
        user_form = CustomUserCreationForm(self.cleaned_data)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            instance.user = user
            if commit:
                instance.save()
            return instance
        raise ValidationError('Invalid User Form')







