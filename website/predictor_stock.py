import numpy as np
import time as tm
import datetime as dt
import tensorflow as tf

# Data preparation
from yahoo_fin import stock_info as yf
from sklearn.preprocessing import MinMaxScaler
from collections import deque

# AI
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

from symbols import technology


def PrepareData(days):
  df = init_df.copy()
  df['future'] = df['close'].shift(-days)
  last_sequence = np.array(df[['close']].tail(days))
  df.dropna(inplace=True)
  sequence_data = []
  sequences = deque(maxlen=N_STEPS)

  for entry, target in zip(df[['close'] + ['date']].values, df['future'].values):
      sequences.append(entry)
      if len(sequences) == N_STEPS:
          sequence_data.append([np.array(sequences), target])

  last_sequence = list([s[:len(['close'])] for s in sequences]) + list(last_sequence)
  last_sequence = np.array(last_sequence).astype(np.float32)

  # construct the X's and Y's
  X, Y = [], []
  for seq, target in sequence_data:
      X.append(seq)
      Y.append(target)

  # convert to numpy arrays
  X = np.array(X)
  Y = np.array(Y)

  return df, last_sequence, X, Y


def GetTrainedModel(x_train, y_train):
  model = Sequential()
  model.add(LSTM(60, return_sequences=True, input_shape=(N_STEPS, len(['close']))))
  model.add(Dropout(0.3))
  model.add(LSTM(120, return_sequences=False))
  model.add(Dropout(0.3))
  model.add(Dense(20))
  model.add(Dense(1))

  BATCH_SIZE = 8
  EPOCHS = 80

  model.compile(loss='mean_squared_error', optimizer='adam')

  model.fit(x_train, y_train,
            batch_size=BATCH_SIZE,
            epochs=EPOCHS,
            verbose=1)

  model.summary()

  return model


def predict_stock_data(sectors, period_type, period_number):
      
  if period_type == "Months":
      LOOKUP_DATE = period_number * 30
  elif period_type == "Years":
      LOOKUP_DATE = period_number * 365

  # GET PREDICTIONS
  predictions = []

  for STOCK in technology:

    # Window size or the sequence length, 7 (1 week)
    N_STEPS = 7

    # Current date
    date_now = tm.strftime('%Y-%m-%d')
    date_5_years_back = (dt.date.today() - dt.timedelta(days=1825)).strftime('%Y-%m-%d')

    # LOAD DATA 
    # from yahoo_fin 
    # for 1104 bars with interval = 1d (one day)
    init_df = yf.get_data(
        STOCK, 
        start_date=date_5_years_back, 
        end_date=date_now, 
        interval='1d')

    # remove columns which our neural network will not use
    init_df = init_df.drop(['open', 'high', 'low', 'adjclose', 'ticker', 'volume'], axis=1)
    # create the column 'date' based on index column
    init_df['date'] = init_df.index

    # Scale data for ML engine
    scaler = MinMaxScaler()
    init_df['close'] = scaler.fit_transform(np.expand_dims(init_df['close'].values, axis=1))
    
    df, last_sequence, x_train, y_train = PrepareData(LOOKUP_DATE)
    x_train = x_train[:, :, :len(['close'])].astype(np.float32)

    model = GetTrainedModel(x_train, y_train)

    last_sequence = last_sequence[-N_STEPS:]
    last_sequence = np.expand_dims(last_sequence, axis=0)
    prediction = model.predict(last_sequence)
    predicted_price = scaler.inverse_transform(prediction)[0][0]

    predictions.append(round(float(predicted_price), 2))


  #if bool(predictions) == True and len(predictions) > 0:
  predictions_list = [str(d)+'$' for d in predictions]
  predictions_str = ', '.join(predictions_list)
  message = f'{STOCK} prediction for upcoming {LOOKUP_DATE} days ({predictions_str})'
      
  return message

temp =predict_stock_data(technology, "Months", 3)
print(temp)
        
