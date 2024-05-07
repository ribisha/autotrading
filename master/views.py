from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup
# import pandas as pd
# from nsepy import get_history
from datetime import datetime
from django.db import IntegrityError      
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from nsetools import Nse
from yahooquery import Ticker
import yfinance as yf
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from urllib.parse import urljoin, unquote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication . models import *
url = 'https://fc.yahoo.com'
response = requests.get(url, timeout=1000)
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password
from client.models import ConnectAPI
# from django_celery_beat.models import PeriodicTask, IntervalSchedule
from master.utils import *
from client.models import * 
from master.tasks import *
from django.http import HttpResponseServerError

from django.shortcuts import get_object_or_404

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def get_real_time_stock_data(symbols):
    stock_data = {}
    for symbol in symbols:
        try:
            data = Ticker(symbol).history(period='1d')
            latest_data = data.iloc[-1]
            stock_data[symbol] = {
                'symbol': symbol,
                'price': latest_data['close'],
                'high': data['high'].max(),
                'low': data['low'].min(),
                'change': latest_data['close'] - data.iloc[0]['open'],
                'change_percent': ((latest_data['close'] - data.iloc[0]['open']) / data.iloc[0]['open']) * 100,
            }
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
    return stock_data
url = "https://finance.yahoo.com/quote/%5ENSEI/components/"
def get_nifty50_data():
    url = "https://finance.yahoo.com/quote/%5ENSEI/components/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"} 
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        nifty50_data = []
        for row in soup.select('table tbody tr'):
            columns = row.find_all('td')
            symbol = columns[0].text.strip()
            company_name = columns[1].text.strip()
            last_price = columns[2].text.strip()
            change = columns[3].text.strip()
            percent_change = columns[4].text.strip()
            volume = columns[5].text.strip()
            nifty50_data.append({
                'symbol': symbol,
                'company_name': company_name,
                'last_price': last_price,
                'change': change,
                'percent_change': percent_change,
                'volume': volume
            })
        return nifty50_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
if __name__ == "__main__":
    nifty50_data = get_nifty50_data()
    if nifty50_data:
        for company_info in nifty50_data:
            print(f"Symbol: {company_info['symbol']}, Company Name: {company_info['company_name']}, "
                  f"Last Price: {company_info['last_price']}, Change: {company_info['change']}, "
                  f"Percent Change: {company_info['percent_change']}, Volume: {company_info['volume']}")
    else:
        print("Error getting Nifty 50 data.")
def nifty_50_stock():
    nifty50_symbols = [
        "ADANIPORTS.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS",
        "BAJAJFINSV.NS", "BHARTIARTL.NS", "BPCL.NS", "BRITANNIA.NS", "CIPLA.NS",
        "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS", "EICHERMOT.NS", "GAIL.NS",
        "GRASIM.NS", "HCLTECH.NS", "HDFC.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
        "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS",
        "INDUSINDBK.NS", "INFY.NS", "IOC.NS", "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS",
        "LT.NS", "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS",
        "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SHREECEM.NS",
        "SUNPHARMA.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS",
        "TITAN.NS", "ULTRACEMCO.NS", "UPL.NS", "WIPRO.NS"
    ]
    master_nifty50_data = []
    for symbol in nifty50_symbols:
        try:
            stock = yf.Ticker(symbol)
            last_price = stock.history(period='1d')['Close'][-1]
            name = stock.info.get('shortName', symbol)
            master_nifty50_data.append({'symbol': symbol, 'name': name, 'last_price': last_price})
        except Exception as e:
            print(f"Failed to fetch data for {symbol}. Error: {e}")
    return master_nifty50_data
    # =================================/

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
@login_required(login_url='master_login')
def index_5_stock(request):
    symbols = ['^NSEI', '^NSEBANK', '^BSESN', 'NIFTY_FIN_SERVICE.NS', '^NSEMDCP50']
    main_component = get_real_time_stock_data(symbols)
    data = [{'symbol': symbol, **stock_data} for symbol, stock_data in main_component.items()]
    return JsonResponse({'data': data})
@login_required(login_url='master_login')
def index_top50_stock(request):
    nifty50_data = get_nifty50_data()
    if nifty50_data:
        top50_stock = {
            'data': [
                {
                    'symbol': info['symbol'],
                    'company_name': info['company_name'],
                    'last_price': info['last_price'],
                    'low': info['change'],
                    'change': info['change'],
                    'percent_change': info['percent_change'],
                }
                for info in nifty50_data
            ]
        }
        return JsonResponse({'top50_stock': top50_stock})
    else:
        return JsonResponse({'error': 'Error getting Nifty 50 data'})
@login_required(login_url='master_login')
def index_master_suggested_stock(request):  
    master_nifty50_data = nifty_50_stock()
    if master_nifty50_data:
        master_nifty50_stock = {
            'data': [
                {
                    'symbol': info['symbol'],
                    'name': info['name'],
                    'last_price': info['last_price'],
                }
                for info in master_nifty50_data
            ]
        }
        return JsonResponse({'master_nifty50_stock': master_nifty50_stock})
    else:
        return JsonResponse({'error': 'Error getting master Nifty 50 data'})
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

@login_required(login_url='master_login')
def dashboard(request):
    return render(request,'master/m_dashboard.html')
# ==========NEWS============
@login_required(login_url='master_login')
def news(request): 
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
        return render(request,'master/news/news.html',{
            'news_list': news_list,
            'articles':articles,
            'most_searched_stocks': most_searched_stocks
            })
    else:
        return render(request,'master/news/news.html',{'error': f"Error: {response.status_code} - {response.reason}"})

# --------------STAFF--------------
@login_required(login_url='master_login')
def master_staff_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not (username and password1 and password1 == password2):
            messages.error(request, 'Invalid input. Please provide a valid username and matching passwords.')
            return redirect('master_staff_add')
        try:
            validate_password(password1)
        except ValidationError as e:
            messages.error(request, f'Password requirements not met: {", ".join(e.messages)}')
            return redirect('master_staff_add')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect('master_staff_add')
        user = User.objects.create_user(username=username)
        user.set_password(password1)
        user.save()
        StaffAccount.objects.create(user_staff=user)
        messages.success(request, 'Form submitted successfully!')
        return redirect('master_staff_add')
    return render(request, 'master/staff/m_add_staff.html')
@login_required(login_url='master_login')
def all_staff(request):
    all_staff_details = StaffAccount.objects.all()
    return render(request,'master/staff/m_all_staff.html',{'all_staff_details':all_staff_details})
@login_required(login_url='master_login')
def staff_profile_management(request,sk):
    staff_profile = StaffAccount.objects.get(id=sk)
    if request.method == 'POST':
        staff_profile.staff_full_name = request.POST.get('staff_full_name', staff_profile.staff_full_name)
        staff_profile.staff_date_of_birth = request.POST.get('staff_date_of_birth', staff_profile.staff_date_of_birth)
        staff_profile.staff_gender = request.POST.get('staff_gender', staff_profile.staff_gender)
        staff_profile.staff_phone = request.POST.get('staff_phone', staff_profile.staff_phone)
        staff_profile.staff_email = request.POST.get('staff_email', staff_profile.staff_email)
        staff_profile.staff_address = request.POST.get('staff_address', staff_profile.staff_address)
        staff_profile.staff_pincode = request.POST.get('staff_pincode', staff_profile.staff_pincode)
        staff_profile.staff_district = request.POST.get('staff_district', staff_profile.staff_district)
        staff_profile.staff_state = request.POST.get('staff_state', staff_profile.staff_state)
        staff_profile.staff_occupation = request.POST.get('staff_occupation', staff_profile.staff_occupation)
        staff_profile.staff_parent_name = request.POST.get('staff_parent_name', staff_profile.staff_parent_name)
        staff_profile.staff_nominee_name = request.POST.get('staff_nominee_name', staff_profile.staff_nominee_name)
        staff_profile.staff_nominee_relationship = request.POST.get('staff_nominee_relationship', staff_profile.staff_nominee_relationship)
        if 'staff_profile_image' in request.FILES:
            staff_profile.staff_profile_image = request.FILES['staff_profile_image']
        staff_profile.save()
    return render(request,'master/staff/m_staff_management.html',{'staff_profile':staff_profile})
@login_required(login_url='master_login')
def m_staff_delete_user(request, staff_user_id):
    staff = get_object_or_404(StaffAccount, id=staff_user_id)
    if request.method == 'POST':
        staff.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('all_staff')
    else:
        return redirect('all_staff')
# --------------END_STAFF-----------------------------------------------------------------

 # --------------CLIENT--------------------------------------------------------------------
   
        
@login_required(login_url='master_login')
def master_client_add(request):
 
    return render(request, 'master/client/m_add_client.html')

#__________________________________________________________________________________________________________________________

#----------------------------------All student users---------------------------------------------------

@login_required(login_url='master_login')
def all_accepted_client(request):
    all_client_details = MasterClientadd.objects.all()
    return render(request,'master/client/m_all_client.html',{'all_client_details':all_client_details})


#_________________________________________________________________________________________________________

#--------------------------------------------------------------------------------------------------
@login_required(login_url='master_login')
def client_profile_management(request,pk):
    client_profile = ClientAccount.objects.get(id=pk)
    if request.method == 'POST':
        client_profile.client_full_name = request.POST.get('client_full_name', client_profile.client_full_name)
        client_profile.client_date_of_birth = request.POST.get('client_date_of_birth', client_profile.client_date_of_birth)
        client_profile.client_gender = request.POST.get('client_gender', client_profile.client_gender)
        client_profile.client_phone = request.POST.get('client_phone', client_profile.client_phone)
        client_profile.client_email = request.POST.get('client_email', client_profile.client_email)
        client_profile.client_address = request.POST.get('client_address', client_profile.client_address)
        client_profile.client_pincode = request.POST.get('client_pincode', client_profile.client_pincode)
        client_profile.client_district = request.POST.get('client_district', client_profile.client_district)
        client_profile.client_state = request.POST.get('client_state', client_profile.client_state)
        client_profile.client_occupation = request.POST.get('client_occupation', client_profile.client_occupation)
        client_profile.client_parent_name = request.POST.get('client_parent_name', client_profile.client_parent_name)
        client_profile.client_nominee_name = request.POST.get('client_nominee_name', client_profile.client_nominee_name)
        client_profile.client_nominee_relationship = request.POST.get('client_nominee_relationship', client_profile.client_nominee_relationship)
        if 'client_profile_image' in request.FILES:
            client_profile.client_profile_image = request.FILES['client_profile_image']
        client_profile.save()
    return render(request,'master/client/m_client_profile.html',{'client_profile':client_profile})

#___________________________________________________________________________________________________________

@login_required(login_url='master_login')
def m_client_delete_user(request, user_id):
    client = get_object_or_404(ClientAccount, id=user_id)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('all_client')
    else:
        return redirect('all_client')
    
# --------------END_CLIENT--------------

# --------------FINANCE--------------
@login_required(login_url='master_login')
def master_finance_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not (username and password1 and password1 == password2):
            messages.error(request, 'Invalid input. Please provide a valid username and matching passwords.')
            return redirect('master_finance_add')
        try:
            validate_password(password1)
        except ValidationError as e:
            messages.error(request, f'Password requirements not met: {", ".join(e.messages)}')
            return redirect('master_finance_add')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect('master_finance_add')
        user = User.objects.create_user(username=username)
        user.set_password(password1)
        user.save()
        FinanceAccount.objects.create(user_finance=user)
        messages.success(request, 'Form submitted successfully!')
        return redirect('master_finance_add')
    return render(request, 'master/finance/m_add_finance.html')
@login_required(login_url='master_login')
def all_finance(request):
    all_finance_details = FinanceAccount.objects.all()
    return render(request,'master/finance/m_all_finance.html',{'all_finance_details':all_finance_details})
@login_required(login_url='master_login')
def master_finance_user_delete(request,finance_user_id):
    finance = get_object_or_404(FinanceAccount, id=finance_user_id)
    if request.method == 'POST':
        finance.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('all_finance')
    else:
        return redirect('all_finance')
# --------------END_FINANCE--------------

# --------------MASTER--------------
def master_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                master_account = MasterAccount.objects.get(user_master=user)
                login(request, user)
                messages.success(request, f"Welcome, {master_account.full_name}!")
                return redirect('dashboard')  
            except ObjectDoesNotExist:
                messages.error(request, "No MasterAccount found for the given user.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request,'auth/login.html')

#--------------------------------------------------------------------------------
@login_required(login_url='master_login')
def master_logout(request):
    logout(request)
    return redirect('master_login')
#--------------------------------------------------------------------------------

@login_required(login_url='master_login')
def master_open_account(request):
    user = request.user
    try:
        master_account = MasterAccount.objects.get(user_master=user)
    except MasterAccount.DoesNotExist:
        master_account = MasterAccount(user_master=user)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        profile_image = request.FILES.get('profile_image')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        district = request.POST.get('district')
        state = request.POST.get('state')
        occupation = request.POST.get('occupation')
        parent_name = request.POST.get('parent_name')
        nominee_name = request.POST.get('nominee_name')
        nominee_relationship = request.POST.get('nominee_relationship')
        if not full_name:
            messages.error(request, 'Full Name is required.')
            return redirect('my_account_master')
        master_account.full_name = full_name
        master_account.profile_image = profile_image
        master_account.date_of_birth = date_of_birth
        master_account.gender = gender
        master_account.phone = phone
        master_account.email = email
        master_account.address = address
        master_account.pincode = pincode
        master_account.district = district
        master_account.state = state
        master_account.occupation = occupation
        master_account.parent_name = parent_name
        master_account.nominee_name = nominee_name
        master_account.nominee_relationship = nominee_relationship
        try:
            master_account.save()
            messages.success(request, 'Profile information updated successfully!')
            return redirect('master_open_account')
        except Exception as e:
            messages.error(request, f'Error saving data: {str(e)}')
            print(f'Error saving data: {str(e)}')
    return render(request,'master/profile/m_open_account.html',{'master_account': master_account})


#----------------------------MASTER OPEN ACCOUNT-------------------------------------------

@login_required(login_url='master_login')
def my_account_master(request):
    master_personal_details = MasterAccount.objects.all()
    user = request.user
    try:
        edit_master_account = MasterAccount.objects.get(user_master=user)
    except MasterAccount.DoesNotExist:
        edit_master_account = MasterAccount(user_master=user)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        profile_image = request.FILES.get('profile_image')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        district = request.POST.get('district')
        state = request.POST.get('state')
        occupation = request.POST.get('occupation')
        parent_name = request.POST.get('parent_name')
        nominee_name = request.POST.get('nominee_name')
        nominee_relationship = request.POST.get('nominee_relationship')
        if not full_name:
            messages.error(request, 'Full Name is required.')
            return redirect('my_account_master')
        edit_master_account.full_name = full_name
        edit_master_account.profile_image = profile_image
        edit_master_account.date_of_birth = date_of_birth
        edit_master_account.gender = gender
        edit_master_account.phone = phone
        edit_master_account.email = email
        edit_master_account.address = address
        edit_master_account.pincode = pincode
        edit_master_account.district = district
        edit_master_account.state = state
        edit_master_account.occupation = occupation
        edit_master_account.parent_name = parent_name
        edit_master_account.nominee_name = nominee_name
        edit_master_account.nominee_relationship = nominee_relationship
        try:
            edit_master_account.save()
            messages.success(request, 'Profile information updated successfully!')
            return redirect('my_account_master')
        except Exception as e:
            messages.error(request, f'Error saving data: {str(e)}')
    return render(request, 'master/profile/m_profile.html', {
        'master_personal_details': master_personal_details,
        'edit_master_account': edit_master_account,
    })
    
    
#--------------------------Angelone Connection---------------------------------
def m_select_broker(request):
    if request.method == 'POST':
        selected_broker = request.POST.get('m_broker')
        print("Selected broker:", selected_broker)
        return redirect('m_connect_api', m_broker=selected_broker)

    return render(request, 'master/profile/master_select_broker.html')


@login_required
def m_connect_api(request, m_broker):
    if request.method == 'POST':

        m_api_key = request.POST.get('m_api_key')
        m_client_id = request.POST.get('m_client_id')
        m_pin = request.POST.get('m_pin') 
        m_qr_value = request.POST.get('m_qr_value')

        m_auth_data = connect_with_broker(m_api_key, m_client_id, m_pin, m_qr_value)
        if m_auth_data:
            m_fetched_data = m_fetch_data_view(m_api_key, m_client_id, m_pin, m_qr_value)
            if m_fetched_data:
                auth_token = m_auth_data['authToken']
                m_balance_data = m_fetch_balance_data(m_api_key, m_client_id, m_pin, m_qr_value)
                if m_balance_data:
                    m_trade_data = m_fetch_trade_data(m_api_key, m_client_id, m_pin, m_qr_value)

                    m_option_data = m_fetch_option_data(m_api_key, m_client_id, m_pin, m_qr_value)
                    
                    try:
                       
                        MasterConnectAPI.objects.update_or_create( 
                            user=request.user,
                            m_broker=m_broker,
                            m_api_key=m_api_key,
                            m_client_id=m_client_id,
                            m_pin=m_pin,
                            m_qr_value=m_qr_value,
                            
                            defaults={
                                'auth_token': auth_token,
                                'm_fetched_data': m_fetched_data,
                                'm_balance_data': m_balance_data,
                                'm_trade_data': m_trade_data,
                                'm_option_data': m_option_data
                            }
                        )
                        messages.success(request, 'Data saved successfully.')
                        
                        place_trade_order(request)
                        
                    except Exception as e:
                       
                        messages.error(request, "An error occurred while saving data.")
                        print(e)
                        
                    create_or_update_periodic_task(m_api_key, m_client_id, m_pin, m_qr_value)
                    
                    
                    return redirect('m_fetched_data')
                else:
                    messages.error(request, 'Failed to fetch balance data.')
            else:
                messages.error(request, 'Failed to fetch data from the broker account.')
        else:
            messages.error(request, 'Failed to connect with your broker account. Please try again.')

    return render(request, 'master/profile/master_connect_api.html', {'m_broker': m_broker})




# @login_required
# def m_connect_api(request, m_broker):
#     if request.method == 'POST':

#         m_api_key = request.POST.get('m_api_key')
#         m_client_id = request.POST.get('m_client_id')
#         m_pin = request.POST.get('m_pin') 
#         m_qr_value = request.POST.get('m_qr_value')

#         m_auth_data = connect_with_broker(m_api_key, m_client_id, m_pin, m_qr_value)
#         if m_auth_data:
#             m_fetched_data = m_fetch_data_view(m_api_key, m_client_id, m_pin, m_qr_value)
#             if m_fetched_data:
#                 auth_token = m_auth_data['authToken']
#                 m_balance_data = m_fetch_balance_data(m_api_key, m_client_id, m_pin, m_qr_value)
#                 if m_balance_data:
#                     m_trade_data = m_fetch_trade_data(m_api_key, m_client_id, m_pin, m_qr_value)

#                     m_option_data = m_fetch_option_data(m_api_key, m_client_id, m_pin, m_qr_value)
                    
#                     try:
                       
#                         MasterConnectAPI.objects.update_or_create( 
#                             user=request.user,
#                             m_broker=m_broker,
#                             m_api_key=m_api_key,
#                             m_client_id=m_client_id,
#                             m_pin=m_pin,
#                             m_qr_value=m_qr_value,
                            
#                             defaults={
#                                 'auth_token': auth_token,
#                                 'm_fetched_data': m_fetched_data,
#                                 'm_balance_data': m_balance_data,
#                                 'm_trade_data': m_trade_data,
#                                 'm_option_data': m_option_data
#                             }
#                         )
#                         messages.success(request, 'Data saved successfully.')
     
                        
#                     except Exception as e:
                       
#                         messages.error(request, "An error occurred while saving data.")
#                         print(e)
                        
#                     create_or_update_periodic_task(m_api_key, m_client_id, m_pin, m_qr_value)
                    
                    
#                     return redirect('m_fetched_data')
#                 else:
#                     messages.error(request, 'Failed to fetch balance data.')
#             else:
#                 messages.error(request, 'Failed to fetch data from the broker account.')
#         else:
#             messages.error(request, 'Failed to connect with your broker account. Please try again.')

#     return render(request, 'master/profile/master_connect_api.html', {'m_broker': m_broker})



#_____________________________________________________________________________________________________

#----------------------------------Fetched Datas----------------------------------------------------


def m_fetched_datas(request):
    connect_data = MasterConnectAPI.objects.filter(user=request.user).first()

    m_fetched_data = None
    m_balance_data = None
    m_trade_data = None
    m_option_data = None
    
    if connect_data:
        m_fetched_data = connect_data.m_fetched_data
        m_balance_data = connect_data.m_balance_data
        m_trade_data = connect_data.m_trade_data
        m_option_data = connect_data.m_option_data
        print(m_trade_data)
        print(m_option_data)

    
    return render(request, 'master/profile/master_fetched_data.html', {'fetched_data': m_fetched_data, 'balance_data': m_balance_data, 'trade_data': m_trade_data, 'option_data':m_option_data})

#__________________________________________________________________________________________________________

#----------------o----------------------------All Client users--------------------------------------------

def display_connected_users(request): 
    connected_users = ConnectAPI.objects.all()
    print(connected_users) 
    return render(request, 'master/client/angelone_connected_clients.html', {'connected_users': connected_users})


def accept_reject(request):
    return render(request, 'master/follow_request.html')  


#_______________________________________________________________________________________________________________

#-------------------------------------------------Add student users----------------------------------------------

@login_required
def connect_now(request):
    
    try:
        client_id = request.POST.get('client_id')
        
        connectapi_instance = get_object_or_404(ConnectAPI, client_id=client_id)
        client_user = connectapi_instance.user
        MasterClientadd.objects.create(
            user=client_user, 
            broker=connectapi_instance.broker,
            api_key=connectapi_instance.api_key,
            client_id=connectapi_instance.client_id,
            pin=connectapi_instance.pin,
            qr_value=connectapi_instance.qr_value,
            auth_token=connectapi_instance.auth_token,
            fetched_data=connectapi_instance.fetched_data,
            balance_data=connectapi_instance.balance_data,
            trade_data=connectapi_instance.trade_data,
            option_data=connectapi_instance.option_data
        )
        return redirect('/')
    except ConnectAPI.DoesNotExist:
        return render(request, 'angelone_connected_clients.html')

#_______________________________________________________________________________________________________________

#-------------------------------------------Auto Trade----------------------------------------------------------


def place_trade_order(request): 
    try: 

        master_client_add_instances = MasterClientadd.objects.all()


        for master_client_add_instance in master_client_add_instances:
            api_key = master_client_add_instance.api_key
            client_id = master_client_add_instance.client_id
            pin = master_client_add_instance.pin
            qr_value = master_client_add_instance.qr_value


            print(f"API Key: {api_key}, Client ID: {client_id}, PIN: {pin}, QR Value: {qr_value}")

        connect_api_instance = MasterConnectAPI.objects.get(user=request.user)

        m_option_data = connect_api_instance.m_option_data

        order_statuses = []

        if m_option_data and 'data' in m_option_data:
            for option in m_option_data['data']:
                order_params = {
                    "variety": "NORMAL",
                    "tradingsymbol": option.get('tradingsymbol'),
                    "symboltoken": option.get('symboltoken'), 
                    "transactiontype": "BUY",  
                    "exchange": option.get('exchange'),
                    "ordertype": "MARKET",
                    "producttype": "CARRYFORWARD",
                    "duration": "DAY",
                    # "price": option.get('ltp'),
                    "squareoff": "0",
                    "stoploss": "0",
                    "quantity": option.get('netqty')
                }
                order_response = place_order(api_key, client_id, pin, qr_value, order_params)

                if order_response:
                    order_statuses.append(f"Order placed successfully for symbol: {option.get('tradingsymbol')}")
                else:
                    order_statuses.append(f"Failed to place order for symbol: {option.get('tradingsymbol')}")
        else:
            order_statuses.append("No option data found")  

        context = {'order_statuses': order_statuses} 
        return render(request, 'master/place_order.html', context)
    except MasterClientadd.DoesNotExist:
        return HttpResponseServerError("MasterClientadd instance not found for the specified user.")
    except MasterConnectAPI.DoesNotExist:
        return HttpResponseServerError("MasterConnectAPI instance not found for the current user.")
    except Exception as e:
        return HttpResponseServerError(f"An error occurred: {str(e)}") 
#______________________________________________________________________________________________________

#----------------------------------Create Room---------------------------------------------------------

@login_required(login_url='master_login')
def create_room(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not (username and password1 and password1 == password2):
            messages.error(request, 'Invalid input. Please provide a valid username and matching passwords.')
            return render(request, 'master/m_create_room.html', {'error_message': 'Invalid input'})
        try:
            validate_password(password1) 
        except ValidationError as e:
            messages.error(request, f'Password requirements not met: {", ".join(e.messages)}')
            return render(request, 'master/m_create_room.html', {'error_message': 'Password requirements not met.'})
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'master/m_create_room.html', {'error_message': 'Username already exists.'})
        user = User.objects.create(username=username, password=password1)
        CreateRoom.objects.create(master_room=user)     
        messages.success(request, 'Form submitted successfully!')
        return redirect('/')
    return render(request, 'master/m_create_room.html')


def all_room(request): 
    all_room_master = CreateRoom.objects.all()
    print(all_room_master)
    return render(request, 'master/m_all_rooms.html', {'all_room_master': all_room_master})

#-----------------------------------------------------------------------------------------------------

@login_required(login_url='master_login')
def master_create_courses(request):
    courses_details = Courses.objects.all() 
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_price = request.POST.get('course_price')
        course_image = request.FILES.get('course_image')
        course = Courses.objects.create(
            course_name=course_name,
            course_price=course_price,
            course_image=course_image
        )
        return redirect('master_create_courses') 
    
    return render(request, 'master/courses/m_create_courses.html',{
        'courses_details':courses_details,
    })
# --------------END_MASTER--------------

# =======================MASTER ACCOUNT CREATE FUNCTION
def master_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'master/register.html')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match. Please enter matching passwords.')
            return render(request, 'master/register.html')
        try:
            user = User.objects.create_user(username=username, password=password)
            master_account = MasterAccount.objects.create(
                user_master=user,
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('/')
        except IntegrityError as e:
            messages.error(request, 'Error creating user. Please try again.')
            return render(request, 'master/register.html')
    return render(request, 'master/register.html')
# ====================== MASTER ACCOUNT CREATE 
