import serial
import mysql.connector
import time

while True:
    db_connection = mysql.connector.connect(
        host='trashcan.mysql.database.azure.com',
        port=3306,
        user='trashcanweb',
        password='Cxb4991mysql',
        database='protest'
    )

    cursor = db_connection.cursor()

    query = "SELECT result_type FROM object_recognition ORDER BY id DESC LIMIT 1"
    cursor.execute(query)

    result = cursor.fetchone()

    if result:
        type = result[0]

        cursor.close()
        db_connection.close()

        ser = serial.Serial('COM4', 9600)  
        # 要傳送的數據
        type = str(type)
        # 將數據傳送到Arduino
        ser.write(type.encode())
        # 關閉串口
        ser.close()
    else:
        print("没有找到最近插入的数据")
        
    time.sleep(3)  