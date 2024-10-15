from django.shortcuts import render
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.db.models import Q
from store.models import *
from .forms import ProductForm

class HomepageView(View):
    def get(self, request):
        products = Products.objects.all()

        return render(request, 'homepage.html', {
            'products': products
        })
    
class ProductListView(View):
    def get(self, request):
        products = Products.objects.all()
    
        # Get the selected product type from the request
        selected_product_type = request.GET.get('product_type', None)

        # If a product type is selected, filter the products
        if selected_product_type:
            products = products.filter(product_type=selected_product_type)

        # Get unique product types for the filter dropdown
        product_types = Products.objects.values_list('product_type', flat=True).distinct()

        context = {
            'products': products,
            'product_types': product_types,
            'selected_product_type': selected_product_type,
        }
        return render(request, 'products.html', context)

class ProductDetailView(View):
    def get(self, request, product_id):
        product_details = Products.objects.get(pk=product_id)

        return render(request, 'product_detail.html', {'product_details': product_details})

class AddProductView(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'product_form.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('products')

class DelProduct(View):
    def get(self, request, product_id):
        product = Products.objects.get(pk=product_id)
        product.delete()
        return redirect('products')

class UpdateProduct(View):
    def get(self, request, product_id):
        product = Products.objects.get(pk=product_id)
        form = ProductForm(instance=product)
        return render(request, 'product_form.html', {'form': form})

    def post(self, request, product_id):
        product = Products.objects.get(pk=product_id)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')

        return render(request, 'product_form.html', {'form': form})


class ProfileView(View):
    def get(self, request):
        # user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        # form = UserProfileForm(instance=user_profile)
        
        # context = {
        #     'user_profile': user_profile,
        #     'form': form,
        # }
        return render(request, 'profile.html')

    # def post(self, request):
        # user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        # form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        # if form.is_valid():
        #     form.save()
        #     return redirect('profile')
        
        # context = {
        #     'user_profile': user_profile,
        #     'form': form,
        # }
        # return render(request, 'profile.html', context)

class Loginpage(View):
    def get(self, request):
        return render(request, 'login.html')
