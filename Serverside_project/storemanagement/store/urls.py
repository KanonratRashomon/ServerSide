from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('change_pass/', views.ChangePassword.as_view(), name='change_password'),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path('homepage/', views.HomepageView.as_view(), name='homepage'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update_profile', views.UserProfileUpdateView.as_view(), name='update_profile'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('cart/<int:product_id>/', views.CartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:product_id>/',  views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('order/history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/add_product/', views.AddProductView.as_view(), name='new_product'),
    path('products/<int:product_id>', views.ProductDetailView.as_view(), name='product_details'),
    path('products/<int:product_id>/remove_product/', views.DelProduct.as_view(), name='remove_product'),
    path('products/<int:product_id>/update_product/', views.UpdateProduct.as_view(), name='update_product'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
