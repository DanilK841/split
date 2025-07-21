from django import forms
from django.contrib.auth.models import Group
from .models import CostDetail, People

# class ProductForm(forms.Form):
#     name = forms.CharField()
#     price = forms.DecimalField(min_value=1, max_value=190000)
#     description = forms.CharField(widget=forms.Textarea)

class CostDetailForm(forms.ModelForm):
    class Meta:
        model = CostDetail
        fields = "name", "people_cost","price", "people_share"
        widgets = {
            'people_share': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        # Извлекаем pk из kwargs перед передачей в родительский класс
        self.pk = kwargs.pop('pk', None)
        super().__init__(*args, **kwargs)

        # Если pk передан - применяем фильтрацию
        if self.pk:
            self.fields['people_cost'].queryset = People.objects.filter(
                cost=self.pk
            )
            self.fields['people_share'].queryset = People.objects.filter(
                cost=self.pk
            )
class CostDetailFormCreate(forms.ModelForm):
    class Meta:
        model = CostDetail
        fields = "name", "people_cost","price", "people_share"
        widgets = {
            'people_share': forms.CheckboxSelectMultiple
        }
    def __init__(self, *args, **kwargs):
        # Извлекаем pk из kwargs перед передачей в родительский класс
        self.pk = kwargs.pop('pk', None)
        super().__init__(*args, **kwargs)

        # Если pk передан - применяем фильтрацию


        if self.pk:
            self.fields['people_cost'].queryset = People.objects.filter(
                cost=self.pk
            )
            self.fields['people_share'].queryset = People.objects.filter(
                cost=self.pk
            )
            self.fields['people_share'].initial = People.objects.filter(
                cost=self.pk
            )