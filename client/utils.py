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
def connect_with_broker(api_key, client_id, pin, qr_value):
    try:
        smartApi = SmartConnect(api_key)
        totp = pyotp.TOTP(qr_value).now()
        data = smartApi.generateSession(client_id, pin, totp)
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
    
#--------------------------Fetch Profile Datas-------------------------------------------------
def fetch_data_view(api_key, client_id, pin, qr_value):
    try:
        # Establish connection with the broker API using provided credentials
        smartApi = SmartConnect(api_key)
        totp = pyotp.TOTP(qr_value).now()
        data = smartApi.generateSession(client_id, pin, totp)
        
        # Check if session establishment was successful
        if data['status']:
            # Fetch user profile data
            profile_data = smartApi.getProfile(data['data']['refreshToken'])
            return profile_data
        else:
            print("Failed to establish session with the broker API.")
            return None
    except Exception as e:
        print("An error occurred while connecting to the broker API:", e)
        return None
    
#--------------------------Fetch Balnace Datas-------------------------------------------------
    
def fetch_balance_data(api_key, client_id, pin, qr_value):
    try:
        # Establish connection with the broker API using provided credentials
        smartApi = SmartConnect(api_key)
        totp = pyotp.TOTP(qr_value).now()
        data = smartApi.generateSession(client_id, pin, totp)
        
        # Check if session establishment was successful
        if data['status']:
            # Fetch balance data
            balance_data = smartApi.rmsLimit()  # Remove the argument here
            return balance_data
        else:
            print("Failed to establish session with the broker API.")
            return None
    except Exception as e:
        print("An error occurred while connecting to the broker API:", e)
        return None
    
#--------------------------Fetch Trade Datas-------------------------------------------------

def fetch_trade_data(api_key, client_id, pin, qr_value):
    try:
        # Establish connection with the broker API using provided credentials
        smartApi = SmartConnect(api_key)
        totp = pyotp.TOTP(qr_value).now()
        data = smartApi.generateSession(client_id, pin, totp)
        
        # Check if session establishment was successful
        if data['status']:
            # Fetch trade data
            trade_data = smartApi.holding()
            return trade_data
        
        else:
            print("Failed to establish session with the broker API.")
            return None
    except Exception as e:
        print("An error occurred while connecting to the broker API:", e)
        return None

def fetch_option_data(api_key, client_id, pin, qr_value):
    try:
        # Establish connection with the broker API using provided credentials
        smartApi = SmartConnect(api_key)
        totp = pyotp.TOTP(qr_value).now()
        data = smartApi.generateSession(client_id, pin, totp)
        
        # Check if session establishment was successful
        if data['status']:
            # Fetch option data
            option_data = smartApi.position()
            return option_data
        
        else:
            print("Failed to establish session with the broker API.")
            return None
    except Exception as e:
        print("An error occurred while connecting to the broker API:", e)
        return None
    

#---------------------------------------------------------------------------
# def place_order(api_key, client_id, pin, qr_value, order_params):
#     try:
#         # Establish connection with the broker API using provided credentials
#         smartApi = SmartConnect(api_key)
        
#         # Generate TOTP for authentication
#         totp = pyotp.TOTP(qr_value).now()
        
#         # Generate session with the broker API
#         data = smartApi.generateSession(client_id, pin, totp)
        
#         # Check if session establishment was successful
#         if data['status']:
#             # Place order
#             order_response = smartApi.placeOrder(order_params)
#             return order_response
#         else:
#             print("Failed to establish session with the broker API.")
#             return None
#     except Exception as e:
#         print("An error occurred while placing the order:", e)
#         return None
#-------------------------------------------------------------------------------


















