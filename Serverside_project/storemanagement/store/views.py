from django.shortcuts import render
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.db.models import Q
from store.models import *

class HomepageView(View):
    def get(self, request):
        products = Products.objects.all()

        return render(request, "homepage.html", {
            "products": products
        })

class ProductDetailView(View):
    def get(self, request, product_id):
        product_details = Products.objects.get(pk=product_id)

        return render(request, "product_detail.html", {
            "product_details": product_details
        })
