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

class AddToCartView(View):
    login_url = '/login/'
    permission_required = ["store.view_products"]
    def post(self, request, product_id):
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            messages.error(request, "สินค้าที่คุณพยายามเพิ่มไม่มีในระบบ.")
            return redirect('products')

        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))

        if str(product_id) in cart:
            cart[str(product_id)] += quantity 
        else:
            cart[str(product_id)] = quantity 
            
        request.session['cart'] = cart
        messages.success(request, f'เพิ่มสินค้าลงในตะกร้าเรียบร้อยแล้ว: {product.title} จำนวน {quantity} ชิ้น')
        
        return redirect('cart')  # Redirect to cart view

class CartView(View):
    login_url = '/login/'
    permission_required = ["store.view_products"]
    def get(self, request):
        cart = request.session.get('cart', {})
        cart_items = []
        total = 0

        for product_id, quantity in cart.items():
            try:
                product = Products.objects.get(id=product_id)
                subtotal = product.get_discounted_price() * quantity
                total += subtotal
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': subtotal
                })
            except Products.DoesNotExist:
                messages.warning(request, f'Product ID {product_id} not found.')

        context = {
            'cart_items': cart_items,
            'total': total,
        }
        return render(request, 'cart.html', context)

    def post(self, request, product_id):
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))
        if str(product_id) in cart:
            cart[str(product_id)] += quantity 
            messages.info(request, f'เพิ่มสินค้า ID {product_id} จำนวน {quantity} ชิ้นในตะกร้าแล้ว')
        else:
            cart[str(product_id)] = quantity
            messages.success(request, f'เพิ่มสินค้า ID {product_id} ลงในตะกร้าแล้ว: {quantity} ชิ้น')

        request.session['cart'] = cart
        return redirect('cart')

class RemoveFromCartView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["store.view_products"]

    def post(self, request, product_id):
        print(f"Request to remove product ID: {product_id}")
        cart = request.session.get('cart', {})
        print(f"Current cart: {cart}")

        if str(product_id) in cart:
            if cart[str(product_id)] > 1:
                cart[str(product_id)] -= 1
            else:
                del cart[str(product_id)]
        else:
            print(f"Product ID {product_id} not in cart")

        request.session['cart'] = cart
        return redirect('cart')

class CheckoutView(View):
    login_url = '/login/'
    permission_required = ["store.view_products"]
    def post(self, request):
        cart = request.session.get('cart', {})
        total = 0

        # คำนวณราคารวมจากตะกร้า
        for product_id, quantity in cart.items():
            try:
                product = Products.objects.get(id=product_id)
                total += product.get_discounted_price() * quantity
            except Products.DoesNotExist:
                messages.error(request, f'สินค้า ID {product_id} ไม่พบ')
                return redirect('cart')

        # แสดงข้อความสำเร็จ
        messages.success(request, f'คุณมีสินค้าที่จะชำระเงินทั้งหมด: ฿{total}')
        
        # ลบสินค้าจากตะกร้า
        request.session['cart'] = {}  # ลบสินค้าทั้งหมดออกจากตะกร้า หรือเปลี่ยนตามต้องการ

        return redirect('products')  # เปลี่ยนเส้นทางไปยังหน้าสินค้า

    def get(self, request):
        cart = request.session.get('cart', {})
        total = 0
        cart_items = []

        for product_id, quantity in cart.items():
            try:
                product = Products.objects.get(id=product_id)
                subtotal = product.get_discounted_price() * quantity
                total += subtotal
                cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
            except Products.DoesNotExist:
                messages.error(request, f'สินค้า ID {product_id} ไม่พบ')
                continue

        return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})
