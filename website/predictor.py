import numpy as np
import time as tm
import datetime as dt
import tensorflow as tf

# Data preparation
#from yahoo_fin import stock_info as yf
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from collections import deque

# AI
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout


def fetch_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    data.reset_index(inplace=True)

    # Convert Timestamp objects to strings
    data['Date'] = data['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    result = data.to_dict('records')

    return result

    
