from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from store.models import *
from django import forms

class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = [
            'title',
            'description',
            'product_category',
            'price',
            'stock_quantity',
            'release_date',
            'added_by_employee',
            'product_image'
        ]
        widgets = {
            'release_date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.is_staff = True
    #     if commit:
    #         user.save()
    #         # เพิ่มผู้ใช้เข้าไปในกลุ่ม Staff
    #         staff_group = Group.objects.get(name='Customer')  # สร้างกลุ่มถ้ายังไม่มี
    #         user.groups.add(staff_group)  # เพิ่มผู้ใช้เข้าไปในกลุ่ม
    #     return user

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already used')
        return email
