from django.shortcuts import render,HttpResponse
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import socket
from nsepy import get_history
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
# nse_data_fetcher.py
from nsetools import Nse
from alpha_vantage.timeseries import TimeSeries

import pandas as pd


def get_real_time_stock_data(api_key, symbols):
    ts = TimeSeries(key=api_key, output_format='pandas')

    stock_data = {}
    for symbol in symbols:
        try:
            data, meta_data = ts.get_quote_endpoint(symbol=symbol)

            price = data.get('05. price', 'N/A')
            change = data.get('09. change', 'N/A')
            change_percent = data.get('10. change percent', 'N/A')

            stock_data[symbol] = {
                'price': price,
                'change': change,
                'change_percent': change_percent
            }
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            
    return stock_data