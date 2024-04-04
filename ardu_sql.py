import serial
import mysql.connector

# 設置資料庫連接訊息
db_connection = mysql.connector.connect(
    host='trashcan.mysql.database.azure.com',
    port = 3306,
    user='trashcanweb',
    password='Cxb4991mysql',
    database='protest'
)

cursor = db_connection.cursor()

# 打開串行端口
ser = serial.Serial('COM7', 9600)  
start = 0
while start==0:
    data = ser.readline().decode('utf-8').strip()
    if data.startswith("DATA,"):
        data = data.split(",")
        distance1 = float(data[1])
        distance2 = float(data[2])
        distance3 = float(data[3])
        distance4 = float(data[4])
        
        cursor.execute("SELECT COUNT(*) FROM sensor_data_1")
        current_count = cursor.fetchone()[0]
        if current_count >= 20:
            delete_query = "DELETE FROM sensor_data_1 ORDER BY id ASC LIMIT %s"
            cursor.execute(delete_query, (current_count - 19,))
        cursor.execute("SELECT COUNT(*) FROM sensor_data_2")
        current_count = cursor.fetchone()[0]
        if current_count >= 20:
            delete_query = "DELETE FROM sensor_data_2 ORDER BY id ASC LIMIT %s"
            cursor.execute(delete_query, (current_count - 19,))
        cursor.execute("SELECT COUNT(*) FROM sensor_data_3")
        current_count = cursor.fetchone()[0]
        if current_count >= 20:
            delete_query = "DELETE FROM sensor_data_3 ORDER BY id ASC LIMIT %s"
            cursor.execute(delete_query, (current_count - 19,))
        cursor.execute("SELECT COUNT(*) FROM sensor_data_4")
        current_count = cursor.fetchone()[0]
        if current_count >= 20:
            delete_query = "DELETE FROM sensor_data_4 ORDER BY id ASC LIMIT %s"
            cursor.execute(delete_query, (current_count - 19,))

        cursor.execute("INSERT INTO sensor_data_1 (distance_value) VALUES (%s)", (distance1,))
        cursor.execute("INSERT INTO sensor_data_2 (distance_value) VALUES (%s)", (distance2,))
        cursor.execute("INSERT INTO sensor_data_3 (distance_value) VALUES (%s)", (distance3,))
        cursor.execute("INSERT INTO sensor_data_4 (distance_value) VALUES (%s)", (distance4,))

        db_connection.commit()
        strat=1
        
    
    # time.sleep(5)

cursor.close()
db_connection.close()