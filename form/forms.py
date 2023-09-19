from django import forms
from .models import ChartUserprofile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = ChartUserprofile
        fields = ['name', 'email','content']