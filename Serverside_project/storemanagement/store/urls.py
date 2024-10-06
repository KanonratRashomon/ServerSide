from django.urls import path

from store import views

urlpatterns = [
    path('homepage/', views.HomepageView.as_view(), name='homepage'),
    path('products/<int:product_id>', views.ProductDetailView.as_view(), name='product_details'),
]
