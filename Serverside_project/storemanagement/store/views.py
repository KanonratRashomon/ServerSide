from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from store.models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
class HomepageView(View):
    def get(self, request):
        products = Products.objects.all()

        return render(request, 'homepage.html', {
            'products': products
        })
    
class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["store.view_products"]
    def get(self, request):
        products = Products.objects.all()
    
        # Get the selected product type from the request
        selected_category = request.GET.get('category', None)

        # If a product type is selected, filter the products
        if selected_category:
            products = products.filter(product_category__id=selected_category)

        # Get unique product types for the filter dropdown
        categories = Category.objects.all()

        context = {
            'products': products,
            'categories': categories,
            'selected_category': selected_category,
        }
        return render(request, 'products.html', context)

class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["store.view_products"]
    def get(self, request, product_id):
        product_details = Products.objects.get(pk=product_id)

        return render(request, 'product_detail.html', {'product_details': product_details})

class AddProductView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["store.add_products"]
    def get(self, request):
        form = ProductForm()
        return render(request, 'product_form.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('products')

class DelProduct(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["store.delete_products"]
    def get(self, request, product_id):
        product = Products.objects.get(pk=product_id)
        product.delete()
        return redirect('products')

class UpdateProduct(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["store.change_products"]
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


class ProfileView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["store.view_products"]
    def get(self, request):
        user = User.objects.get(username=request.user)
        return render(request, 'profile.html', {'user': user})
    
class UserProfileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ['store.view_products']
    def get(self, request):
        user = request.user
        form = UserProfileForm(instance=user)

        return render(request, 'profile_form.html', {'form': form})

    def post(self, request):
        user = request.user
        form = UserProfileForm(request.POST, instance=user)
        
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request, 'profile_form.html', {'form': form})

class Register(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})

class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('homepage')  

        return render(request,'login.html', {"form":form})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('homepage')

class ChangePassword(View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for keeping the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'change_password.html', {'form': form})

class AddToCartView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["store.view_products"]
    def post(self, request, product_id):
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return redirect('products')

        quantity = int(request.POST.get('quantity', 1))

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': 0, 'user': request.user if request.user.is_authenticated else None}
            )

            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                cart[str(product_id)] += quantity
            else:
                cart[str(product_id)] = quantity
            
            request.session['cart'] = cart
        return redirect('cart')


class CartView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["store.view_products"]
    def get(self, request):
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(cart__user=request.user)
            total = sum(item.product.get_discounted_price() * item.quantity for item in cart_items)
        else:
            cart = request.session.get('cart', {})
            cart_items = []
            total = 0

            for product_id, quantity in cart.items():
                product = Products.objects.get(id=product_id)
                subtotal = product.get_discounted_price() * quantity
                total += subtotal
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': subtotal
                })

        context = {
            'cart_items': cart_items,
            'total': total,
        }

        return render(request, 'cart.html', context)

    def post(self, request, product_id):
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return redirect('cart')

        quantity = int(request.POST.get('quantity', 1))

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': 0, 'user': request.user}
            )
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                cart[str(product_id)] += quantity
            else:
                cart[str(product_id)] = quantity
            request.session['cart'] = cart

        return redirect('cart')

class RemoveFromCartView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["store.view_products"]
    def post(self, request, product_id):
        if request.user.is_authenticated:
            try:
                # Retrieve the cart associated with the authenticated user
                cart = Cart.objects.get(user=request.user)
                cart_item = CartItem.objects.get(cart=cart, product_id=product_id)

                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()

            except Cart.DoesNotExist:
                messages.error(request, "ไม่พบตะกร้าของคุณ.")
                return redirect('cart')
            except CartItem.DoesNotExist:
                messages.error(request, "สินค้าที่คุณพยายามลบไม่มีในตะกร้า.")
                return redirect('cart')

        else:
            # Handle cases for anonymous users (session-based cart)
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                if cart[str(product_id)] > 1:
                    cart[str(product_id)] -= 1
                else:
                    del cart[str(product_id)]
            else:
                messages.error(request, "สินค้าที่คุณพยายามลบไม่มีในตะกร้า.")

            request.session['cart'] = cart

        messages.success(request, "ลบสินค้าจากตะกร้าเรียบร้อยแล้ว")
        return redirect('cart')



class CheckoutView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["store.view_products"]
    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
        except Cart.DoesNotExist:
            cart_items = []

        total_price = sum(item.product.get_discounted_price() * item.quantity for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return render(request, 'checkout.html', context)

    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
        except Cart.DoesNotExist:
            messages.error(request, "ไม่พบสินค้าในตะกร้า")
            return redirect('view_cart')

        if not cart_items:
            messages.error(request, "ตะกร้าของคุณว่างเปล่า")
            return redirect('view_cart')

        total_price = sum(item.product.get_discounted_price() * item.quantity for item in cart_items)

        # สร้าง Order
        order = Order.objects.create(user=request.user, total_price=total_price)

        # ย้ายข้อมูลจาก CartItem ไปยัง OrderItem
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.get_discounted_price()
            )

        # ล้าง Cart
        cart.items.all().delete()
        cart.delete()

        messages.success(request, "การสั่งซื้อของคุณเสร็จสมบูรณ์")
        return redirect('order_history')

class OrderHistoryView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["store.view_products"]
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'order_history.html', {'orders': orders})


