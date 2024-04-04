import os
import mysql.connector
from datetime import datetime
import time

i = 0

# 初始化最高信心程度和對應的結果
best_confidence = -1  # 初始設定一個極低的信心程度
best_result = None

while True:
    folder_path = f'exp{i}/labels'  # 資料夾路徑

    # 檢查資料夾是否存在
    if os.path.exists(folder_path):
        txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

        for txt_file in txt_files:
            with open(os.path.join(folder_path, txt_file), 'r') as file:
                line = file.readline().strip().split()

                if len(line) == 5:
                    result_type = int(line[0])
                    confidence = float(line[4])

                    # 檢查當前結果的信心程度是否比目前最高信心程度更高
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_result = (line, confidence)

        # 連接到MySQL資料庫
        conn = mysql.connector.connect(
            host='trashcan.mysql.database.azure.com',
            port=3306,
            user='trashcanweb',
            password='Cxb4991mysql',
            database='protest'
        )
        cursor = conn.cursor()

        if best_result:
            # 插入信心程度最高的結果到SQL
            sql = "INSERT INTO object_recognition (result_type, confidence) VALUES (%s, %s)"
            data = (best_result[0][0], best_result[1])  # 插入數據格式

            cursor.execute(sql, data)
            conn.commit()

        # 關閉資料庫連接
        conn.close()

        i += 1  # 前進到下一個資料夾

    # 每隔一段時間檢查一次新資料夾，避免過度監控
    time.sleep(60)