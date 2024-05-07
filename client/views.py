from multiprocessing import AuthenticationError
import SmartApi
from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.db import IntegrityError
from django.contrib import messages
from authentication.models import *
from django.core.exceptions import ObjectDoesNotExist
from master. models import *
from django.contrib.auth.decorators import login_required
from master.views import*
from .models import *  
from logzero import logger
import requests
from SmartApi import SmartConnect
import pyotp
import logging
import json
from client.utils import connect_with_broker,fetch_data_view, fetch_balance_data, fetch_trade_data, fetch_option_data
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from django.http import Http404
from master.tasks import *

# -----------AUTH-----------
def client_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                client_account = ClientAccount.objects.get(user_client=user)
                login(request, user)
                messages.success(request, f"Welcome, {client_account.client_full_name}!")
                return redirect('client_dashboard')  
            except ObjectDoesNotExist:
                messages.error(request, "No MasterAccount found for the given user.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'client/auth/c_login.html')

#________________________________________________________________________________________________

def client_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'client/auth/c_register.html')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match. Please enter matching passwords.')
            return render(request, 'client/auth/c_register.html')
        try:
            user = User.objects.create_user(username=username, password=password)
            client_account = ClientAccount.objects.create(
                user_client=user,
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('client_login')
        except IntegrityError as e:
            messages.error(request, 'Error creating user. Please try again.')
            return render(request, 'client/auth/c_register.html')
    return render(request,'client/auth/c_register.html')

#____________________________________________________________________________________________


#=====================API connection & Fetching=====================================#

def select_broker(request):
    if request.method == 'POST': 
        selected_broker = request.POST.get('broker')
        print("Selected broker:", selected_broker)
        return redirect('connect_api', broker=selected_broker)

    return render(request, 'client/profile/select_broker.html')


@login_required
def connect_api(request, broker):
    if request.method == 'POST':
        # Fetch form data
        api_key = request.POST.get('api_key')
        client_id = request.POST.get('client_id')
        pin = request.POST.get('pin')
        qr_value = request.POST.get('qr_value')

        auth_data = connect_with_broker(api_key, client_id, pin, qr_value)
        if auth_data:
            fetched_data = fetch_data_view(api_key, client_id, pin, qr_value)
            if fetched_data:
                auth_token = auth_data['authToken']
                balance_data = fetch_balance_data(api_key, client_id, pin, qr_value)
                if balance_data:
                    trade_data = fetch_trade_data(api_key, client_id, pin, qr_value)

                    option_data = fetch_option_data(api_key, client_id, pin, qr_value)
                    
                    try:
                       
                        ConnectAPI.objects.update_or_create(
                            user=request.user,
                            broker=broker,
                            api_key=api_key,
                            pin = pin,
                            qr_value=qr_value,
                            client_id=client_id,
                            defaults={
                                'auth_token': auth_token,
                                'fetched_data': fetched_data,
                                'balance_data': balance_data,
                                'trade_data': trade_data,
                                'option_data': option_data
                            }
                        )
                        messages.success(request, 'Data saved successfully.')
     
                        
                    except Exception as e:
                       
                        messages.error(request, "An error occurred while saving data.")
                        print(e)
                        
                    create_or_update_periodic_task(api_key, client_id, pin, qr_value)
                    
                    
                    return redirect('fetched_data')
                else:
                    messages.error(request, 'Failed to fetch balance data.')
            else:
                messages.error(request, 'Failed to fetch data from the broker account.')
        else:
            messages.error(request, 'Failed to connect with your broker account. Please try again.')

    return render(request, 'client/profile/connect_api.html', {'broker': broker})

#____________________________________________________________________________________________________________

def fetched_datas(request):
    connect_data = ConnectAPI.objects.filter(user=request.user).first()

    fetched_data = None
    balance_data = None
    trade_data = None
    option_data = None
    
    if connect_data:
        fetched_data = connect_data.fetched_data
        balance_data = connect_data.balance_data
        trade_data = connect_data.trade_data
        option_data = connect_data.option_data
        print(trade_data)
        print(option_data)

    
    return render(request, 'client/profile/fetched_data.html', {'fetched_data': fetched_data, 'balance_data': balance_data, 'trade_data': trade_data, 'option_data':option_data})


#___________________________________________________________________________________


# def place_trade_order(request):
   
#     return render(request, 'master/place_order.html')

#_____________________________________________________________________________________________________

@login_required(login_url='client_login')
def client_open_account(request):
    user = request.user
    try:
        client_account = ClientAccount.objects.get(user_client=user)
    except ClientAccount.DoesNotExist:
        client_account = ClientAccount(user_client=user)
    if request.method == 'POST':
        full_name = request.POST.get('client_full_name')
        profile_image = request.FILES.get('client_profile_image')
        date_of_birth = request.POST.get('client_date_of_birth')
        gender = request.POST.get('client_gender')
        phone = request.POST.get('client_phone')
        email = request.POST.get('client_email')
        address = request.POST.get('client_address')
        pincode = request.POST.get('client_pincode')
        district = request.POST.get('client_district')
        state = request.POST.get('client_state')
        occupation = request.POST.get('client_occupation')
        parent_name = request.POST.get('client_parent_name')
        nominee_name = request.POST.get('client_nominee_name')
        nominee_relationship = request.POST.get('client_nominee_relationship')
        if not full_name:  # Fix this line
            messages.error(request, 'Full Name is required.')
            return redirect('client_open_account')
        client_account.client_full_name = full_name
        client_account.client_profile_image = profile_image
        client_account.client_date_of_birth = date_of_birth
        client_account.client_gender = gender
        client_account.client_phone = phone
        client_account.client_email = email
        client_account.client_address = address
        client_account.client_pincode = pincode
        client_account.client_district = district
        client_account.client_state = state
        client_account.client_occupation = occupation
        client_account.client_parent_name = parent_name
        client_account.client_nominee_name = nominee_name
        client_account.client_nominee_relationship = nominee_relationship
        try:
            client_account.save()
            messages.success(request, 'Profile information updated successfully!')
            return redirect('client_open_account')
        except Exception as e:
            messages.error(request, f'Error saving data: {str(e)}')
            print(f'Error saving data: {str(e)}')
    return render(request, 'client/auth/c_open_account.html', {
        'client_account': client_account
    })

#________________________________________________________________________________________

@login_required(login_url='client_login')
def client_logout(request):
    logout(request)
    return redirect('client_login')

#____________________________________________________________________________________________

@login_required(login_url='client_login')
def client_dashboard(request):
    return render(request,'client/core/c_dahboard.html')

#_____________________________________________________________________________________________
@login_required(login_url='client_login')
@login_required(login_url='client_login')
def c_courses(request):
    if request.method == 'POST':
        user = request.user
        client_account = ClientAccount.objects.get(user_client=user)
        
        selected_course_ids = [course_id for course_id in request.POST.getlist('selected_courses') if course_id]
        for course_id in selected_course_ids:
            course = Courses.objects.get(pk=course_id)
            SelectedCourses.objects.create(client_account=client_account, course=course)
        return redirect('c_courses')
    
    all_courses = Courses.objects.all()
    return render(request, 'client/core/c_courses.html', {
        'all_courses': all_courses
    })
    
#______________________________________________________________________________________________
@login_required(login_url='client_login')
def c_profile(request):
    client_personal_details = ClientAccount.objects.all()
    user = request.user
    try:
        client_account = ClientAccount.objects.get(user_client=user)
    except ClientAccount.DoesNotExist:
        client_account = ClientAccount(user_client=user)
    if request.method == 'POST':
        full_name = request.POST.get('client_full_name')
        profile_image = request.FILES.get('client_profile_image')
        date_of_birth = request.POST.get('client_date_of_birth')
        gender = request.POST.get('client_gender')
        phone = request.POST.get('client_phone')
        email = request.POST.get('client_email')
        address = request.POST.get('client_address')
        pincode = request.POST.get('client_pincode')
        district = request.POST.get('client_district')
        state = request.POST.get('client_state')
        occupation = request.POST.get('client_occupation')
        parent_name = request.POST.get('client_parent_name')
        nominee_name = request.POST.get('client_nominee_name')
        nominee_relationship = request.POST.get('client_nominee_relationship')
        if not full_name:
            messages.error(request, 'Full Name is required.')
            return redirect('client_open_account')
        client_account.client_full_name = full_name
        client_account.client_profile_image = profile_image
        client_account.client_date_of_birth = date_of_birth
        client_account.client_gender = gender
        client_account.client_phone = phone
        client_account.client_email = email
        client_account.client_address = address
        client_account.client_pincode = pincode
        client_account.client_district = district
        client_account.client_state = state
        client_account.client_occupation = occupation
        client_account.client_parent_name = parent_name
        client_account.client_nominee_name = nominee_name
        client_account.client_nominee_relationship = nominee_relationship        
        try:
            client_account.save()
            messages.success(request, 'Profile information updated successfully!')
            return redirect('c_profile')
        except Exception as e:
            messages.error(request, f'Error saving data: {str(e)}')

    return render(request,'client/profile/c_profile.html',{
        'client_personal_details':client_personal_details,
        'client_account':client_account
    })

# ==================NEWS
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@login_required(login_url='client_login')
def client_news(request):
    url = "https://economictimes.indiatimes.com/markets/stocks/news"  
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return render(request, 'debug/news_details.html', {'error': f"Request Error: {e}"})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        stories = soup.find_all('div', class_='eachStory')
        news_list = []
        for story in stories:
            img_url = story.find('img')['src']
            heading = story.find('h3').find('a').text
            article_url = story.find('h3').find('a')['href']
            timestamp = story.find('time', class_='date-format')['data-time']
            description = story.find('p').text
            absolute_url = urljoin(url, article_url)
            news_list.append({
                'img_url': img_url,
                'heading': heading,
                'article_url': absolute_url, 
                'timestamp': timestamp,
                'description': description,
            })
        # ========MOST POPULER NEWS================
        articles = []
        for li in soup.find_all('li'):
            title_element = li.find('a', class_='hl')
            img_element = li.find('img')
            if title_element and img_element:
                title = title_element.get('title')
                img_url = img_element.get('src')
                articles.append({'title': title, 'img_url': img_url})
        # ============Most Searched Stocks=============
        most_searched_stocks = []
        most_searched_section = soup.find('section', class_='mostSearchedStocks')
        if most_searched_section:
            for row in most_searched_section.find_all('tr'):
                columns = row.find_all('td')
                if len(columns) == 2:
                    stock_name_anchor = columns[0].find('a')
                    stock_name = stock_name_anchor.text.strip() if stock_name_anchor else ""
                    stock_value = columns[1].text.strip()
                    datetime_stock_span = row.find('span', class_='dateTimeStock')
                    datetime_stock = datetime_stock_span.text.strip() if datetime_stock_span else ""
                    percentage_change_span = columns[1].find('span', class_='per')
                    percentage_change = percentage_change_span.text.strip() if percentage_change_span else ""
                    stock_data = {
                        'stock_name': stock_name,
                        'stock_value': stock_value,
                        'datetime_stock': datetime_stock,
                        'percentage_change': percentage_change,
                    }
                    most_searched_stocks.append(stock_data)
            items_per_page = 13
            paginator = Paginator(most_searched_stocks, items_per_page)
            page = request.GET.get('page', 1)
            try:
                most_searched_stocks = paginator.page(page)
            except PageNotAnInteger:
                most_searched_stocks = paginator.page(1)
            except EmptyPage:
                most_searched_stocks = paginator.page(paginator.num_pages)
        return render(request,'client/news/c_news.html',{
            'news_list': news_list,
            'articles':articles,
            'most_searched_stocks': most_searched_stocks
            })
    else:
        return render(request,'master/news/news.html',{'error': f"Error: {response.status_code} - {response.reason}"})

# ==================STOCK DATA

from django.http import HttpResponse, JsonResponse
@login_required(login_url='client_login')
def client_index_5_stock(request):
    symbols = ['^NSEI', '^NSEBANK', '^BSESN', 'NIFTY_FIN_SERVICE.NS', '^NSEMDCP50']
    main_component = get_real_time_stock_data(symbols)
    data = [{'symbol': symbol, **stock_data} for symbol, stock_data in main_component.items()]
    return JsonResponse({'data':data})
@login_required(login_url='client_login')
def client_index_top50_stock(request):
    pass
login_required(login_url='client_login')
def client_index_master_suggested_stock(request):
    pass


def all_client(request):
    pass