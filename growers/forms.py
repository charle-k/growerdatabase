
from django import forms


from .models import Province, District


class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ['name', ]


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['name', 'province', ]


class FileForm(forms.Form):
    upload = forms.FileField(label='Upload File for Processing')
