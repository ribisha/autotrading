from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import MasterAccount

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')

        if password != confirm_password:
            return render(request, 'registration/register.html', {'error_message': 'Passwords do not match'})
        if len(password) < 8:
            return render(request, 'registration/register.html', {'error_message': 'Password should be at least 8 characters'})
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html', {'error_message': 'Username already exists'})

        user, created = User.objects.get_or_create(
            username=username,
            email=email,  # Set the email explicitly
            defaults={'password': make_password(password)}
        )

        if created:
            # Create MasterAccount instance with the user_master relationship
            master_account = MasterAccount.objects.create(user_master=user)
            
            authenticated_user = authenticate(request, username=username, password=password)
            login(request, authenticated_user)
            return redirect('/')
        return render(request, 'registration/register.html', {'error_message': 'Username already exists'})

    # If it's a GET request, just render the registration form
    return render(request, 'registration/register.html')
