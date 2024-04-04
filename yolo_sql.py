import mysql.connector
import cv2
import torch
from models.yolov5 import YOLOv5  # 导入自己训练的YOLOv5模型

# 连接到MySQL数据库
conn = mysql.connector.connect(
    host='trashcan.mysql.database.azure.com',
    port = 3306,
    user='trashcanweb',
    password='Cxb4991mysql',
    database='protest'
)

cursor = conn.cursor()

# 加载自己训练的YOLOv5模型权重文件
model_weights = 'path_to_your_model_weights.pt'  # 替换为您自己训练的权重文件路径
yolo = YOLOv5(model_weights=model_weights)

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # 使用自己训练的YOLOv5模型进行实时辨识
    results = yolo(frame)

    for result in results:
        class_name, confidence, bbox = result
        x_min, y_min, x_max, y_max = bbox

        # 插入结果到数据库
        insert_query = "INSERT INTO garbage_classification (class, confidence) VALUES (%s, %s)"
        insert_data = (class_name, confidence)
        cursor.execute(insert_query, insert_data)

    # 提交更改到数据库
    conn.commit()

    # 在图像上绘制辨识结果
    for result in results:
        class_name, confidence, bbox = result
        x_min, y_min, x_max, y_max = bbox
        cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
        cv2.putText(frame, f"{class_name} ({confidence:.2f})", (int(x_min), int(y_min) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 显示图像
    cv2.imshow('YOLOv5 Real-time Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 关闭连接和摄像头
conn.close()
cap.release()
cv2.destroyAllWindows()





