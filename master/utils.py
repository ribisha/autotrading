from SmartApi import SmartConnect
from jwt import InvalidTokenError
import pyotp
from logzero import logger
import time
import logging
from requests import HTTPError
import json
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError
import logging
import time
from django.http import request
from.models import *

#--------------------------Connect with Angelone-------------------------------------------------
def connect_with_broker(m_api_key, m_client_id, m_pin, m_qr_value):
    try:
        smartApi = SmartConnect(m_api_key)
        totp = pyotp.TOTP(m_qr_value).now()
        data = smartApi.generateSession(m_client_id, m_pin, totp)
        if data['status'] == False:
            logger.error("Failed to establish session with Angel One broker account.")
            return None
        else:
            authToken = data['data']['jwtToken']
            refreshToken = data['data']['refreshToken']
            return {'authToken': authToken, 'refreshToken': refreshToken}
    except Exception as e:
        logger.exception("Error occurred while connecting with Angel One broker account:")
        return None

#_____________________________________________________________________________________________________
    
#--------------------------Fetch Profile Datas-------------------------------------------------
def m_fetch_data_view(m_api_key, m_client_id, m_pin, m_qr_value):
    try:

        smartApi = SmartConnect(m_api_key)
        totp = pyotp.TOTP(m_qr_value).now()
        data = smartApi.generateSession(m_client_id, m_pin, totp)

        if data['status']:
            # user profile data----fetch-------
            profile_data = smartApi.getProfile(data['data']['refreshToken'])
            return profile_data
        else:
            print("Failed to establish session with the broker API.")
            return None
    except Exception as e:
        print("An error occurred while connecting to the broker API:", e)
        return None

#___________________________________________________________________________________________________
    
#--------------------------Fetch Balnace Datas-------------------------------------------------
    
def m_fetch_balance_data(m_api_key, m_client_id, m_pin, m_qr_value):
    try:
        smartApi = SmartConnect(m_api_key)
        totp = pyotp.TOTP(m_qr_value).now()
        data = smartApi.generateSession(m_client_id, m_pin, totp)
        
        if data['status']:
            balance_data = smartApi.rmsLimit() 
            return balance_data
        else:
            print("Failed to establish session with the broker API.")
            return None
    except Exception as e:
        print("An error occurred while connecting to the broker API:", e)
        return None
    
#______________________________________________________________________________________________
    
#--------------------------Fetch stock Details-------------------------------------------------

def m_fetch_trade_data(m_api_key, m_client_id, m_pin, m_qr_value):
    try:
        smartApi = SmartConnect(m_api_key)
        totp = pyotp.TOTP(m_qr_value).now()
        data = smartApi.generateSession(m_client_id, m_pin, totp)
        
        if data['status']:
            trade_data = smartApi.holding()
            return trade_data
        
        else:
            print("Failed to establish session with the broker API.")
            return None
    except Exception as e:
        print("An error occurred while connecting to the broker API:", e)
        return None

#______________________________________________________________________________________

#-------------------------------Fetch Option data-----------------------------------
def m_fetch_option_data(m_api_key, m_client_id, m_pin, m_qr_value):
    try:
        smartApi = SmartConnect(m_api_key)
        totp = pyotp.TOTP(m_qr_value).now()
        data = smartApi.generateSession(m_client_id, m_pin, totp)
        
        if data['status']:
            option_data = smartApi.position()
            return option_data
        
        else:
            print("Failed to establish session with the broker API.")
            return None
    except Exception as e:
        print("An error occurred while connecting to the broker API:", e)
        return None
    
#____________________________________________________________________________________

#-----------------------------Autotrading-----------------------------------------

def place_order(api_key, client_id, pin, qr_value, order_params):
    try:
        smartApi = SmartConnect(api_key)
        totp = pyotp.TOTP(qr_value).now()
        data = smartApi.generateSession(client_id, pin, totp)
        
        if data['status']:
            order_response = smartApi.placeOrder(order_params)
            return order_response
        else:
            print("Failed to establish session with the broker API.")
            return None
    except Exception as e:
        print("An error occurred while placing the order:", e)
        return None
#_______________________________________________________________________________________





