from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from .forms import UserProfileForm

# Create your views here.
def contact(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()  # 將數據保存到資料庫
        return redirect('index')  # 重新定向成功頁面
    else:
        form = UserProfileForm()

    return render(request, 'contact.html', {'form': form})