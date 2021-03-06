# -*- coding: utf-8 -*-
"""1901-2015.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MBKsHydnavNfrH-oW7vDdxNXcuK1of3x
"""

# Part 1 - Data Preprocessing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io

# Importing the training set
from google.colab import files
uploaded = files.upload()

dataset_train = pd.read_csv(io.BytesIO(uploaded['Maha_1901-2015.csv']))
r = int(input())
if r == 1:
  i_val = r
elif r == 2:
  i_val = r
elif r == 3:
  i_val = r
elif r == 4:
  i_val = r
elif r == 5:
  i_val = r
training_set = dataset_train.iloc[0:1104, i_val:i_val+1].values

dataset_train

training_set.size

# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

# Creating a data structure with 60 timesteps and 1 output
X_train = []
y_train = []
for i in range(60, 1104):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

# Reshaping
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

X_train.size

y_train

# Part 2 - Building the RNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

# Initialising the RNN
regressor = Sequential()

# Adding the first LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 80, return_sequences = True, input_shape = (X_train.shape[1], 1)))
regressor.add(Dropout(0.1))

# Adding a second LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 80, return_sequences = True))
regressor.add(Dropout(0.1))

# Adding a third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 80, return_sequences = True))
regressor.add(Dropout(0.1))

# Adding a fourth LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 80))
regressor.add(Dropout(0.1))

# Adding the output layer
regressor.add(Dense(units = 1))

# Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Fitting the RNN to the Training set
regressor.fit(X_train, y_train, epochs = 20, batch_size = 32)

# Part 3 - Making the predictions and visualising the results

# Getting the real stock price of 2017
#from google.colab import files
#uploaded1 = files.upload()
i_val

dataset_test = pd.read_csv(io.BytesIO(uploaded['Maha_1901-2015.csv']))
dt_1 = dataset_test.iloc[1105:1380, 0].values
real_stock_price = dataset_test.iloc[1105:1380, i_val:i_val+1].values

real_stock_price.size

dt_1.size

dt_1

dataset_total = pd.concat((dataset_train['RAINFALL_KONKAN & GOA'], dataset_test['RAINFALL_KONKAN & GOA']), axis = 0)

inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(60,335):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)
predicted_stock_price[predicted_stock_price<0] = 0
print(predicted_stock_price)



results= []                                                        # Converting an array to list as further I have compiled the code in list.
for k in predicted_stock_price:
  results.append(k[0])
print(results)

c = []
for i in results:                                                  # for getting the accurate data which are above 700mm of rainfall
  if i >= 1100:
    c.append(i)
print(c)
p = [i for i,x in enumerate(results) if x >= 1100]                  # for getting the position of data where the data is above 700mm of rainfall
print(p)
for i in p:                                                        # for printing the months which are having rainfall above 700mm which may cause rainfall
  print(dt_1[i])


# Visualising the results
#KONKAN & GOA Original Rainfall Data
#KONKAN & GOA Predicted Rainfall Data
if i_val == 1:
  plt.plot(real_stock_price, color = 'red', label = '')
  plt.plot(predicted_stock_price, color = 'blue', label = '')
elif i_val == 2:
  plt.plot(real_stock_price, color = 'red', label = 'MADHYA MAHARASHTRA Original Rainfall Data')
  plt.plot(predicted_stock_price, color = 'blue', label = 'MADHYA MAHARASHTRA Predicted Rainfall Data')
elif i_val == 3:
  plt.plot(real_stock_price, color = 'red', label = 'MARATHVADA Original Rainfall Data')
  plt.plot(predicted_stock_price, color = 'blue', label = 'MARATHVADA Predicted Rainfall Data')
elif i_val == 4:
  plt.plot(real_stock_price, color = 'red', label = 'VIDHARBA Original Rainfall Data')
  plt.plot(predicted_stock_price, color = 'blue', label = 'VIDHARBA Predicted Rainfall Data')
elif i_val == 5:
  plt.plot(real_stock_price, color = 'red', label = 'CHHATTISGARH Original Rainfall Data')
  plt.plot(predicted_stock_price, color = 'blue', label = 'CHHATTISGARH Predicted Rainfall Data')
plt.scatter(p,c, marker='>',label='Warning', c='r')
plt.title('Rainfall Prediction')
plt.xlabel('Months')
plt.ylabel('Rainfall in mm')
plt.legend()
plt.show()