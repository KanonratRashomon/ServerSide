from django.urls import path

from store import views

urlpatterns = [
    path('login/', views.Loginpage.as_view(), name='login'),
    path('homepage/', views.HomepageView.as_view(), name='homepage'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('add_product/', views.AddProductView.as_view(), name='new_product'),
    path('products/<int:product_id>', views.ProductDetailView.as_view(), name='product_details'),
    path('products/<int:product_id>/remove_product/', views.DelProduct.as_view(), name='remove_product'),
    path('products/<int:product_id>/update_product/', views.UpdateProduct.as_view(), name='update_product'),
]
