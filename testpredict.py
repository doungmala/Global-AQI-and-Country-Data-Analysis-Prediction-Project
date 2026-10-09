import pandas as pd
import numpy as np

'''
# สร้าง mock dataset
np.random.seed(42)
n = 500
data = pd.DataFrame({
    'PM2.5': np.random.normal(35, 10, n),
    'Temperature': np.random.normal(30, 5, n),
    'Humidity': np.random.normal(70, 10, n),
    'Hour': np.random.randint(0, 24, n)
})
'''
# สมมุติว่าในไฟล์มีคอลัมน์ PM2.5, Temperature, Humidity, Hour
df = pd.read_csv('AQI-and-Lat-Long-of-Countries.csv')

data = df[["AQI Value","CO AQI Value","Ozone AQI Value","NO2 AQI Value","PM2.5 AQI Value","lat","lng"]]
#data = df['PM2.5_next']  # ค่าที่ต้องการพยากรณ์

# ใช้งานต่อกับโมเดลได้เลย


# ค่าที่ต้องการพยากรณ์ (ค่าฝุ่นในอีก 1 ชั่วโมงข้างหน้า)
data['PM2.5_next'] = data['PM2.5 AQI Value'] 

data.head()


from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# แยก features และ target
X = data[["AQI Value","CO AQI Value","Ozone AQI Value","NO2 AQI Value","PM2.5 AQI Value","lat","lng"]]
y = data['PM2.5_next']

# แบ่งข้อมูล train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# สร้างโมเดล
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ทำนาย
y_pred = model.predict(X_test)

# ประเมินผล
print("MSE:", mean_squared_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

import mysql.connector


while True:
    
    # เชื่อมต่อกับฐานข้อมูล
    conn = mysql.connector.connect(
        host='nextsoftwarethailand.com',
        user='nextsoft_dev_01',
        password='nextsoft1234',
        database='nextsoft_dev_01'
    )
    cursor = conn.cursor()

    # รัน SQL query
    cursor.execute("SELECT * FROM activex_db")

    # ดึงข้อมูลทั้งหมด
    rows = cursor.fetchall()

    # แสดงผล
    for row in rows:
        print(row)
        datess = row[1]
        timess = row[2]
        pm = row[3]
        co2 = row[4]
        voc = row[5]
        no2 = row[6]
        temp = row[7]
        humdi = row[8]

    print(datess)
    print(humdi)
    # ปิดการเชื่อมต่อ
    cursor.close()
    conn.close()

    import requests

    # ใส่ API Key ที่ได้จาก OpenWeatherMap
    API_KEY = 'c4a92d0112eb46499a931c3a84aa8b84'

    # พิกัดของพื้นที่ (กรุงเทพฯ)
    lat = 13.7563
    lon = 100.5018

    # สมมุติว่าเซ็นเซอร์ส่งค่ามาแบบนี้
    sample = pd.DataFrame([{
        'AQI Value': 40,
        'CO AQI Value': co2,
        'Ozone AQI Value': 60,
        'NO2 AQI Value': no2,
        'PM2.5 AQI Value': pm,
        'lat': 20,
        'lng': 11
    }])

    prediction = model.predict(sample)
    print("PM2.5 prediction in next hour:", prediction[0])

