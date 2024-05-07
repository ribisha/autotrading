from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from authentication.models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .utils import *
from .tasks import *
from .models import *
from client.models import *
from django.http import HttpResponseServerError
# ------------AUTH------------
def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                staff_account = StaffAccount.objects.get(user_staff=user)
                login(request, user)
                messages.success(request, f"Welcome, {staff_account.user_staff.username}!")
                return redirect('staff_dashboard')  
            except StaffAccount.DoesNotExist:
                messages.error(request, "No StaffAccount found for the given user.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'staff/auth/staff_login.html')
#------------------------------------------------------------------------------------------

@login_required(login_url='staff_login')
def staff_logout(request):
    logout(request)
    return redirect('staff_login')

# ----------------------------------------------------------------------------------------

@login_required(login_url='staff_login')
def staff_dashboard(request):
    return render(request,'staff/dashboard/s_dashboard.html')

# ------------CLIENT-MANAGEMENT----------------------------------------------------------

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
@login_required(login_url='staff_login')
def staff_add_client(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not (username and password1 and password1 == password2):
            messages.error(request, 'Invalid input. Please provide a valid username and matching passwords.')
            return render(request, 'staff/client/s_add_client.html', {'error_message': 'Invalid input'})
        try:
            validate_password(password1)
        except ValidationError as e:
            messages.error(request, f'Password requirements not met: {", ".join(e.messages)}')
            return render(request, 'staff/client/s_add_client.html', {'error_message': 'Password requirements not met.'})
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'staff/client/s_add_client.html', {'error_message': 'Username already exists.'})
        user = User.objects.create(username=username, password=password1)
        ClientAccount.objects.create(user_client=user)     
        messages.success(request, 'Form submitted successfully!')
        return redirect('staff_add_client')
    return render(request,'staff/client/s_add_client.html')
#------------------------------------------------------------------------------------------------------------------

@login_required(login_url='staff_login')
def staff_all_client(request):
    s_all_client = ClientAccount.objects.all()
    return render(request,'staff/client/s_all_staff.html',{
        's_all_client':s_all_client
    })
#------------------------------------------------------------------------------------------------------------

@login_required(login_url='staff_login')
def staff_client_delete_user(request,client_user_id):
    s_client = get_object_or_404(ClientAccount, id=client_user_id)
    if request.method == 'POST':
        s_client.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('staff_all_client')
    else:
        return redirect('staff_all_client')
#------------------------------------------------------------------------------------------------------------

@login_required(login_url='staff_login')
def staff_client_profile_management(request,s_c_m):
    s_client_profile = ClientAccount.objects.get(id=s_c_m)
    if request.method == 'POST':
        s_client_profile.client_full_name = request.POST.get('client_full_name', s_client_profile.client_full_name) or s_client_profile.client_full_name
        s_client_profile.client_date_of_birth = request.POST.get('client_date_of_birth', s_client_profile.client_date_of_birth) or s_client_profile.client_date_of_birth
        s_client_profile.client_gender = request.POST.get('client_gender', s_client_profile.client_gender) or s_client_profile.client_gender
        s_client_profile.client_phone = request.POST.get('client_phone', s_client_profile.client_phone) or s_client_profile.client_phone
        s_client_profile.client_email = request.POST.get('client_email', s_client_profile.client_email) or s_client_profile.client_email
        s_client_profile.client_address = request.POST.get('client_address', s_client_profile.client_address) or s_client_profile.client_address
        s_client_profile.client_pincode = request.POST.get('client_pincode', s_client_profile.client_pincode) or s_client_profile.client_pincode
        s_client_profile.client_district = request.POST.get('client_district', s_client_profile.client_district) or s_client_profile.client_district
        s_client_profile.client_state = request.POST.get('client_state', s_client_profile.client_state) or s_client_profile.client_state
        s_client_profile.client_occupation = request.POST.get('client_occupation', s_client_profile.client_occupation) or s_client_profile.client_occupation
        s_client_profile.client_parent_name = request.POST.get('client_parent_name', s_client_profile.client_parent_name) or s_client_profile.client_parent_name
        s_client_profile.client_nominee_name = request.POST.get('client_nominee_name', s_client_profile.client_nominee_name) or s_client_profile.client_nominee_name
        s_client_profile.client_nominee_relationship = request.POST.get('client_nominee_relationship', s_client_profile.client_nominee_relationship) or s_client_profile.client_nominee_relationship 
        if 'client_profile_image' in request.FILES:
            s_client_profile.client_profile_image = request.FILES['client_profile_image']
        s_client_profile.save()
    return render(request,'staff/client/s_client_profile.html',{
        's_client_profile':s_client_profile
    })
#---------------------------------------------------------------------------------------------------------------------

@login_required(login_url='staff_login')
def staff_client_lead_management(request):
    all_leads = SelectedCourses.objects.all()
    return render(request,'staff/client/s_lead_management.html',{
        'all_leads':all_leads,
    })
#----------------------------------------------------------------------------------------------------------------------

# -----------STAFF_MANAGAEMENT-------------------------------------------------------------------
@login_required(login_url='staff_login')
def staff_profile(request):
    staff_personal_details = StaffAccount.objects.all()
    user = request.user
    try:
        edit_staff_account = StaffAccount.objects.get(user_staff=user)
    except StaffAccount.DoesNotExist:
        edit_staff_account = StaffAccount(user_staff=user)
    if request.method == 'POST':
        full_name = request.POST.get('staff_full_name')
        profile_image = request.FILES.get('staff_profile_image')
        date_of_birth = request.POST.get('staff_date_of_birth')
        gender = request.POST.get('staff_gender')
        phone = request.POST.get('staff_phone')
        email = request.POST.get('staff_email')
        address = request.POST.get('staff_address')
        pincode = request.POST.get('staff_pincode')
        district = request.POST.get('staff_district')
        state = request.POST.get('staff_state')
        occupation = request.POST.get('staff_occupation')
        parent_name = request.POST.get('staff_parent_name')
        nominee_name = request.POST.get('staff_nominee_name')
        nominee_relationship = request.POST.get('staff_nominee_relationship')
        if not full_name:
            messages.error(request, 'Full Name is required.')
            return redirect('staff_profile')
        edit_staff_account.staff_full_name = full_name
        edit_staff_account.staff_profile_image = profile_image
        edit_staff_account.staff_date_of_birth = date_of_birth
        edit_staff_account.staff_gender = gender
        edit_staff_account.staff_phone = phone
        edit_staff_account.staff_email = email
        edit_staff_account.staff_address = address
        edit_staff_account.staff_pincode = pincode
        edit_staff_account.staff_district = district
        edit_staff_account.staff_state = state
        edit_staff_account.staff_occupation = occupation
        edit_staff_account.staff_parent_name = parent_name
        edit_staff_account.staff_nominee_name = nominee_name
        edit_staff_account.staff_nominee_relationship = nominee_relationship
        try:
            edit_staff_account.save()
            messages.success(request, 'Profile information updated successfully!')
            return redirect('staff_profile')
        except Exception as e:
            messages.error(request, f'Error saving data: {str(e)}')

    return render(request, 'staff/profile/staff_profile_management.html', {
        'edit_staff_account': edit_staff_account,
        'staff_personal_details':staff_personal_details
        }
    )
#----------------------------------------------------------------------------------------------------------------------

@login_required(login_url='staff_login')
def staff_open_account(request):
    user = request.user
    try:
        save_staff_account = StaffAccount.objects.get(user_staff=user)
    except StaffAccount.DoesNotExist:
        save_staff_account = StaffAccount(user_staff=user)
    if request.method == 'POST':
        full_name = request.POST.get('staff_full_name')
        profile_image = request.FILES.get('staff_profile_image')
        date_of_birth = request.POST.get('staff_date_of_birth')
        gender = request.POST.get('staff_gender')
        phone = request.POST.get('staff_phone')
        email = request.POST.get('staff_email')
        address = request.POST.get('staff_address')
        pincode = request.POST.get('staff_pincode')
        district = request.POST.get('staff_district')
        state = request.POST.get('staff_state')
        occupation = request.POST.get('staff_occupation')
        parent_name = request.POST.get('staff_parent_name')
        nominee_name = request.POST.get('staff_nominee_name')
        nominee_relationship = request.POST.get('staff_nominee_relationship')
        if not full_name:
            messages.error(request, 'Full Name is required.')
            return redirect('my_account_master')
        save_staff_account.staff_full_name = full_name
        save_staff_account.staff_profile_image = profile_image
        save_staff_account.staff_date_of_birth = date_of_birth
        save_staff_account.staff_gender = gender
        save_staff_account.staff_phone = phone
        save_staff_account.staff_email = email
        save_staff_account.staff_address = address
        save_staff_account.staff_pincode = pincode
        save_staff_account.staff_district = district
        save_staff_account.staff_state = state
        save_staff_account.staff_occupation = occupation
        save_staff_account.staff_parent_name = parent_name
        save_staff_account.staff_nominee_name = nominee_name
        save_staff_account.staff_nominee_relationship = nominee_relationship
        try:
            save_staff_account.save()
            messages.success(request, 'Profile information updated successfully!')
            return redirect('staff_open_account')
        except Exception as e:
            messages.error(request, f'Error saving data: {str(e)}')
    return render(request,'staff/profile/staff_open_account.html',{'save_staff_account':save_staff_account})
#----------------------------------------------------------------------------------------------------------------------


def staff_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'staff/auth/staff_register.html')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match. Please enter matching passwords.')
            return render(request, 'staff/auth/staff_register.html')
        try:
            user = User.objects.create_user(username=username, password=password)
            staff_account = StaffAccount.objects.create(
                user_staff=user,
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('staff_login')
        except IntegrityError as e:
            messages.error(request, 'Error creating user. Please try again.')
            return render(request, 'client/auth/c_register.html')
    return render(request,'staff/auth/staff_register.html')


#-------------------Angelone--------------------------------------

def s_select_broker(request):
    if request.method == 'POST':
        selected_broker = request.POST.get('s_broker')
        print("Selected broker:", selected_broker)
        return redirect('s_connect_api', s_broker=selected_broker)

    return render(request, 'staff/profile/staff_select_broker.html')


@login_required
def s_connect_api(request, s_broker):
    if request.method == 'POST':

        s_api_key = request.POST.get('s_api_key')
        s_client_id = request.POST.get('s_client_id')
        s_pin = request.POST.get('s_pin') 
        s_qr_value = request.POST.get('s_qr_value')

        s_auth_data = connect_with_broker(s_api_key, s_client_id, s_pin, s_qr_value)
        if s_auth_data:
            s_fetched_data = s_fetch_data_view(s_api_key, s_client_id, s_pin, s_qr_value)
            if s_fetched_data:
                auth_token = s_auth_data['authToken']
                s_balance_data = s_fetch_balance_data(s_api_key, s_client_id, s_pin, s_qr_value)
                if s_balance_data:
                    s_trade_data = s_fetch_trade_data(s_api_key, s_client_id, s_pin, s_qr_value)

                    s_option_data = s_fetch_option_data(s_api_key, s_client_id, s_pin, s_qr_value)
                    
                    try:
                       
                        StaffConnectAPI.objects.update_or_create( 
                            user=request.user,
                            s_broker=s_broker,
                            s_api_key=s_api_key,
                            s_client_id=s_client_id,
                            s_pin=s_pin,
                            s_qr_value=s_qr_value,
                            
                            defaults={
                                'auth_token': auth_token,
                                's_fetched_data': s_fetched_data,
                                's_balance_data': s_balance_data,
                                's_trade_data': s_trade_data,
                                's_option_data': s_option_data
                            }
                        )
                        messages.success(request, 'Data saved successfully.')
     
                        
                    except Exception as e:
                       
                        messages.error(request, "An error occurred while saving data.")
                        print(e)
                        
                    create_or_update_periodic_task(s_api_key, s_client_id, s_pin, s_qr_value)
                    
                    
                    return redirect('s_fetched_data')
                else:
                    messages.error(request, 'Failed to fetch balance data.')
            else:
                messages.error(request, 'Failed to fetch data from the broker account.')
        else:
            messages.error(request, 'Failed to connect with your broker account. Please try again.')

    return render(request, 'staff/profile/staff_connect_api.html', {'s_broker': s_broker})


def s_fetched_data(request):
    connect_data = StaffConnectAPI.objects.filter(user=request.user).first()

    s_fetched_data = None
    s_balance_data = None
    s_trade_data = None
    s_option_data = None
    
    if connect_data:
        s_fetched_data = connect_data.s_fetched_data
        s_balance_data = connect_data.s_balance_data
        s_trade_data = connect_data.s_trade_data
        s_option_data = connect_data.s_option_data
        print(s_trade_data)
        print(s_option_data)

    
    return render(request, 'staff/profile/staff_fetched_data.html', {'fetched_data': s_fetched_data, 'balance_data': s_balance_data, 'trade_data': s_trade_data, 'option_data':s_option_data})

def all_clients(request): 
    s_connected_users = ConnectAPI.objects.all()
    print(s_connected_users) 
    return render(request, 'staff/profile/all_clients.html', {'connected_users': s_connected_users})

@login_required
def s_connect_now(request):
    
    try:
        client_id = request.POST.get('client_id')
        
        s_connectapi_instance = get_object_or_404(ConnectAPI, client_id=client_id)
        s_client_user = s_connectapi_instance.user
        StaffClientAdd.objects.create(
            s_client_user=s_client_user, 
            broker=s_connectapi_instance.broker,
            api_key=s_connectapi_instance.api_key,
            client_id=s_connectapi_instance.client_id,
            pin=s_connectapi_instance.pin,
            qr_value=s_connectapi_instance.qr_value,
            auth_token=s_connectapi_instance.auth_token,
            fetched_data=s_connectapi_instance.fetched_data,
            balance_data=s_connectapi_instance.balance_data,
            trade_data=s_connectapi_instance.trade_data,
            option_data=s_connectapi_instance.option_data
        )
        return redirect('/')
    except ConnectAPI.DoesNotExist:
        return render(request, 'staff/profile/all_clients.html')

@login_required(login_url='staff_login')
def s_accepted_client(request):
    staff_client_details = StaffClientAdd.objects.all()
    return render(request,'staff/profile/s_all_clients.html',{'staff_client_details':staff_client_details})


def s_place_trade_order(request): 
    try:

        staff_client_add_instances = StaffClientAdd.objects.all()


        for staff_client_add_instance in staff_client_add_instances:
            api_key = staff_client_add_instance.api_key
            client_id = staff_client_add_instance.client_id
            pin = staff_client_add_instance.pin
            qr_value = staff_client_add_instance.qr_value


            print(f"API Key: {api_key}, Client ID: {client_id}, PIN: {pin}, QR Value: {qr_value}")

        # s_connect_api_instance = StaffConnectAPI.objects.get(s_client_user=request.s_client_user)
        s_connect_api_instance = StaffConnectAPI.objects.get(user=request.user)
        
        s_option_data = s_connect_api_instance.s_option_data 

        order_statuses = []

        if s_option_data and 'data' in s_option_data:
            for option in s_option_data['data']:
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
        return render(request, 'staff/profile/place_order.html', context)
    except StaffClientAdd.DoesNotExist:
        return HttpResponseServerError("MasterClientadd instance not found for the specified user.")
    except StaffConnectAPI.DoesNotExist:
        return HttpResponseServerError("MasterConnectAPI instance not found for the current user.")
    except Exception as e:
        return HttpResponseServerError(f"An error occurred: {str(e)}") 