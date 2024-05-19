from django import forms
from .models import Notification

class NotifyForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('user', 'code', 'rent_url', )


# class RentConditionForm(forms.ModelForm):
#     url = forms.CharField()
#     class Meta:    
#         model = RentCondition    
#         fields = ('url', )