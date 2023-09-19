from django.shortcuts import render
from chart.models import ObjectRecognition
from chart.models import SensorData0,SensorData1,SensorData2,SensorData3,SensorData4
import plotly.graph_objs as go
import pandas as pd
from collections import Counter
from plotly.offline import plot

# Create your views here. 
def type_calaulate():
    #讀取sql資料
	typedf = pd.DataFrame(ObjectRecognition.objects.all().values())
	dftype = typedf['result_type']
	#計算各類數量
	typecoun = Counter(typedf["result_type"])
	typedf2 = pd.DataFrame.from_dict(typecoun,orient='index',columns=["Count"])
	typedf2count=typedf2['Count']
	#轉換類別名稱
	all_count = pd.concat([typedf2count])
	type_name = list(all_count.index)
	for i in range(len(type_name)):
		if type_name[i] == 0 :
			type_name[i] = "玻璃"
		elif type_name[i] == 1 :
			type_name[i] = "鐵鋁"
		elif type_name[i] == 2 :
			type_name[i] = "紙類"
		elif type_name[i] == 3 :
			type_name[i] = "塑膠"
		elif type_name[i] == 4 :
			type_name[i] = "一般"
		else :
			type_name[i] = "紙箱"
	#繪製長條圖
	fig = plot([go.Bar(x = type_name ,
        y = all_count),
        ],output_type='div')

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
    fig = type_calaulate()
    f0_num,f1_num,f2_num,f3_num,f4_num,f0_numpre,f1_numpre,f2_numpre,f3_numpre ,f4_numpre = fullness()
    return render( request, "index.html", locals())

def about(request):
    return render(request,'about.html')