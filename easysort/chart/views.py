from django.shortcuts import render
from chart.models import ObjectRecognition
from chart.models import SensorData0,SensorData1,SensorData2,SensorData3,SensorData4
import plotly.graph_objs as go
import pandas as pd
from collections import Counter
from plotly.offline import plot
import requests
from django.conf import settings

# Create your views here. 
def type_calculate():
    # 讀取sql資料
    typedf = pd.DataFrame(ObjectRecognition.objects.all().values())
    dftype = typedf['result_type']
    
    # 計算各類數量
    typecount = Counter(typedf["result_type"])
    
    # 合併"紙類"和"紙箱"的數量為一個組合類別
    typecount_combined = typecount.copy()
    typecount_combined[2] += typecount_combined[5]  # 紙類和紙箱合併為一個組合類別
    del typecount_combined[5]  # 刪除"紙箱"類別
    
    # 轉換類別名稱
    type_name = {
        0: "玻璃",
        1: "鐵鋁",
        2: "紙類",  # 將"紙類"和"紙箱"組合
        3: "塑膠",
        4: "一般"
    }
    
    type_name_combined = [type_name[i] for i in typecount_combined.keys()]
    
    # 繪製長條圖
    fig = plot([go.Bar(x=type_name_combined, y=list(typecount_combined.values()))], output_type='div')
    
    return fig

def fullness():
    f0df = pd.DataFrame(SensorData0.objects.all().values())
    f0_num = f0df.at[0, 'distance_value']
    f0_numpre = round((f0_num / 30) * 100, 2)
    
    f1df = pd.DataFrame(SensorData1.objects.all().values())
    f1_num = f1df.at[0, 'distance_value']
    f1_numpre = round((f1_num / 30) * 100, 2)

    f2df = pd.DataFrame(SensorData2.objects.all().values())
    f2_num = f2df.at[0, 'distance_value']
    f2_numpre = round((f2_num / 30) * 100, 2)
    
    f3df = pd.DataFrame(SensorData3.objects.all().values())
    f3_num = f3df.at[0, 'distance_value']
    f3_numpre = round((f3_num / 30) * 100, 2)
    
    f4df = pd.DataFrame(SensorData4.objects.all().values())
    f4_num = f4df.at[0, 'distance_value']
    f4_numpre = round((f4_num / 30) * 100, 2)
    
    return f0_num,f1_num,f2_num,f3_num,f4_num,f0_numpre,f1_numpre,f2_numpre,f3_numpre ,f4_numpre  

def index( request ):
    fig = type_calculate()
    f0_num,f1_num,f2_num,f3_num,f4_num,f0_numpre,f1_numpre,f2_numpre,f3_numpre ,f4_numpre = fullness()
    return render( request, "index.html", locals())

def about(request):
    return render(request,'about.html')