from django.urls import path

from store import views

urlpatterns = [
    path('homepage/', views.HomepageView.as_view(), name='homepage'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<int:product_id>', views.ProductDetailView.as_view(), name='product_details'),
]
