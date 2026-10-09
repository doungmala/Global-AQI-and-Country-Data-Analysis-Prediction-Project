import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

data = pd.read_csv('AQI-and-Lat-Long-of-Countries.csv')
print(data.head())

data = data.dropna()
data.columns = [col.strip().lower() for col in data.columns]

sns.pairplot(data)
plt.show()

corr = data.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')

X = data[['co aqi value', 'ozone aqi value', 'no2 aqi value', 'pm2.5 aqi value']]
y = data['aqi value']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

import mysql.connector

mydb = mysql.connector.connect(
host='nextsoftwarethailand.com',
user='nextsoft_dev_01',
password='nextsoft1234',
database='nextsoft_dev_01'
)

mycursor = mydb.cursor()

sql = "INSERT INTO activex_predictAQI (tt,predict_aqi) VALUES (%s,%s)"
val = ('1', str(min(y_pred)))
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")

print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))
print('y_pred : ',sum(y_pred))
plt.figure(figsize=(10, 6))
plt.plot(y_test.values, label='Actual AQI')
plt.plot(y_pred, label='Predicted AQI', alpha=0.7)
plt.title('Actual vs Predicted AQI')
plt.legend()
plt.show()



