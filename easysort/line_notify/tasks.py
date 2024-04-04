from celery import shared_task
from chart.views import fullness
import requests
import time

notification_sent = [False,False,False,False,False]

@shared_task
def send_line_notify(message):
    line_notify_token = 'aDBfjDIGvwvNHvkbxeszfiQuyKkq9o6qYFYAGc391oK'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    
    headers = {
        'Authorization': 'Bearer ' + line_notify_token,
    }

    data = {
        'message': message,
    }

    if not notification_sent[0]:
        response = requests.post(line_notify_api, headers=headers, data=data)
        if response.status_code == 200:
            notification_sent[0] = True
            print('Line Notify 发送通知成功:', message)
        else:
            print('Line Notify 发送通知失败:', response.status_code, response.text)
    else:
        print('通知已发送，垃圾桶0仍然未清空:', message)

while True:
    f0_num ,f1_num ,f2_num ,f3_num ,f4_num = fullness() 
    if f0_num < 8:
        send_line_notify("垃圾桶0即将满溢!")
    elif f0_num > 8:
        # 如果垃圾桶已清空，重置通知状态以便下次触发通知
        notification_sent[0] = False
        
    if f1_num < 8:
        send_line_notify("垃圾桶1即将满溢!")
    elif f1_num > 8:
        # 如果垃圾桶已清空，重置通知状态以便下次触发通知
        notification_sent[1] = False
        
    if f2_num < 8:
        send_line_notify("垃圾桶2即将满溢!")
    elif f2_num > 8:
        # 如果垃圾桶已清空，重置通知状态以便下次触发通知
        notification_sent[2] = False
        
    if f3_num < 8:
        send_line_notify("垃圾桶3即将满溢!")
    elif f3_num > 8:
        # 如果垃圾桶已清空，重置通知状态以便下次触发通知
        notification_sent[3] = False
        
    if f4_num < 8:
        send_line_notify("垃圾桶4即将满溢!")
    elif f4_num > 8:
        # 如果垃圾桶已清空，重置通知状态以便下次触发通知
        notification_sent[4] = False