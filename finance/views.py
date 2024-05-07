from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.db import IntegrityError
from django.contrib import messages
from authentication.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


def finance_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:  
                try:
                    finance_account = FinanceAccount.objects.get(user_finance=user)
                    login(request, user)
                    return redirect('finance_dahboard')
                except FinanceAccount.DoesNotExist:
                    messages.error(request, "No FinanceAccount found for the given user.")
            else:
                messages.error(request, "This account is inactive.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'finance/auth/finance_login.html')
@login_required(login_url='finance_login')
def finance_logout(request):
    logout(request)
    return redirect('finance_login')
@login_required(login_url='finance_login')
def finance_dahboard(request):
    return render(request,'finance/core/finance_dashboard.html')
