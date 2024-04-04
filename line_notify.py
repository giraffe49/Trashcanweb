import mysql.connector
import requests
notification_sent = [False, False, False, False, False]

def send_notification(trashcan_index, distance_value):
    if distance_value <= 8 and not notification_sent[trashcan_index]:
        notification_sent[trashcan_index] = True
        print(notification_sent, distance_value)
        line_notify_token = "HGJbwbWoEcorcThEru6uJnIcGMVsE4vzZKTKVwI8XNb"
        message = f"垃圾桶{trashcan_index}要吐了!!!"
        line_notify_api = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {line_notify_token}"}
        data = {"message": message}
        response = requests.post(line_notify_api, headers=headers, data=data)
    elif distance_value > 8 and notification_sent[trashcan_index]:
        notification_sent[trashcan_index] = False
        print(notification_sent, distance_value)
        line_notify_token = "HGJbwbWoEcorcThEru6uJnIcGMVsE4vzZKTKVwI8XNb"
        message = f"垃圾桶{trashcan_index}已清理!!!"
        line_notify_api = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": f"Bearer {line_notify_token}"}
        data = {"message": message}
        response = requests.post(line_notify_api, headers=headers, data=data)

while True:
    # 連接MySQL數據庫
    conn = mysql.connector.connect(
        host='trashcan.mysql.database.azure.com',
        port=3306,
        user='trashcanweb',
        password='Cxb4991mysql',
        database='protest'
    )

    # 創建游標對象
    cursor = conn.cursor()

    for trashcan_index in range(5):
        # 查詢 sensor_data_N 中最新的 distance_value
        query = f"SELECT distance_value FROM sensor_data_{trashcan_index} ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            distance_value = result[0]

            send_notification(trashcan_index, distance_value)

    # 關閉數據庫連接
    conn.close()