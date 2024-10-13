from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, SplitDateTimeWidget
from django.core.exceptions import ValidationError
from store.models import *
from django import forms

class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = [
            'title',
            'description',
            'product_type',
            'price',
            'stock_quantity',
            'release_date',
            'added_by_employee'
        ]
        widgets = {
            'release_date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
