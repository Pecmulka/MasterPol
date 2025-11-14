from django import forms
from .models import Product_type, Material_type

class MaterialCalculatorForm(forms.Form):
    product_type = forms.ModelChoiceField(
        queryset=Product_type.objects.all(),
        label="Тип продукции",
        widget=forms.Select(attrs={'class': 'uk-select'})
    )
    material_type = forms.ModelChoiceField(
        queryset=Material_type.objects.all(),
        label="Тип материала",
        widget=forms.Select(attrs={'class': 'uk-select'})
    )
    product_quantity = forms.IntegerField(
        min_value=1,
        label="Количество продукции",
        widget=forms.NumberInput(attrs={'class': 'uk-input', 'min': '1'})
    )
    param1 = forms.FloatField(
        min_value=0.01,
        label="Параметр 1",
        widget=forms.NumberInput(attrs={'class': 'uk-input', 'step': '0.01', 'min': '0.01'})
    )
    param2 = forms.FloatField(
        min_value=0.01,
        label="Параметр 2",
        widget=forms.NumberInput(attrs={'class': 'uk-input', 'step': '0.01', 'min': '0.01'})
    )