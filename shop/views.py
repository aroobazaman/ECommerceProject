from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required 
from .forms import ProductForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages

class RegisterView(View):
    def get(self, request):
        return render(request, 'shop/register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'shop/register.html')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "User created successfully. Please log in.")
        return redirect('login')

def about_view(request):
    return render(request, 'shop/about.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})



# @api_view(['POST'])
# def login_view(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(request, username=username, password=password)
    
#     if user is not None:
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         })
#     else:
#         return Response({'error': 'Invalid Credentials'}, status=400)
    
@csrf_exempt
@api_view(['POST'])
def custom_login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
   

def logout_view(request):
    logout(request)
    return redirect('login')





def product_list(request):
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

# @login_required
# def cart_add(request, product_id):
#     product = get_object_or_404(Product, id=product_id, available=True)
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#     return redirect('cart_detail')

@login_required
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    order = Order.objects.create(user=request.user, total=0)
    total = 0
    for item in cart.items.all():
        OrderItem.objects.create(order=order, product=item.product, price=item.product.price, quantity=item.quantity)
        total += item.product.price * item.quantity
    order.total = total
    order.save()
    cart.items.all().delete()  # Empty the cart
    return render(request, 'shop/checkout.html', {'order': order})


from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm 
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required


from .models import Product

def search(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    return render(request, 'shop/search_results.html', {'results': results, 'query': query})

def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form})  
from django.shortcuts import render
from django.http import HttpResponse 
from .models import Product, Cart, CartItem


def product_image_upload(request):
    # Your view logic for handling image uploads goes here
    return HttpResponse("Product image upload page")

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')
 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    
def home(request):
    return render(request, 'home.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view."})

# views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import UserToken

# class CustomTokenObtainPairView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         if response.status_code == status.HTTP_200_OK:
#             user = request.user
#             tokens = response.data
#             access_token = tokens['access']
#             refresh_token = tokens['refresh']

#             # Calculate the expiration time for the access token
#             expires_at = timezone.now() + timedelta(minutes=5)

#             # Save the tokens to the database
#             UserToken.objects.create(
#                 user=user,
#                 access_token=access_token,
#                 refresh_token=refresh_token,
#                 expires_at=expires_at
#             )

#         return response


# views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class RevokeTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        try:
            user_token = UserToken.objects.get(access_token=token)
            user_token.delete()
            return Response({"detail": "Token revoked successfully."}, status=status.HTTP_200_OK)
        except UserToken.DoesNotExist:
            return Response({"detail": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)


# shop/views.py
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import JsonResponse

class JWTLoginView(View):
    def get(self, request):
        return render(request, 'shop/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            login(request, user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            # return JsonResponse(response_data)
            return  redirect('/')
        
            # return render(request, 'shop/dashboard.html', {'response_data':  response_data})
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

# shop/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view."})



# shop/views.py
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import login
from django.shortcuts import render, redirect

# class RegisterView(View):
#     def get(self, request):
#         return render(request, 'shop/register.html')

#     def post(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')

#         if User.objects.filter(username=username).exists():
#             return JsonResponse({"error": "Username already exists"}, status=400)
        
#         user = User.objects.create_user(username=username, password=password, email=email)
#         user.save()

#         return JsonResponse({"message": "User created successfully"})

class LogoutView(View):
    def post(self, request):
        response = JsonResponse({"message": "Logout successful"})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
    

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.middleware.csrf import get_token


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.middleware.csrf import get_token

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = redirect('product_list')  # Redirect to the desired page
            response.set_cookie('access_token', str(refresh.access_token))
            response.set_cookie('refresh_token', str(refresh))
            return response
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials'})
    return render(request, 'login.html', {'csrf_token': get_token(request)})

# def logout_view(request):
#     response = redirect('login')  # Redirect to the login page after logout
#     response.delete_cookie('access_token')
#     response.delete_cookie('refresh_token')
#     return response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access',
            value=serializer.validated_data['access'],
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh',
            value=serializer.validated_data['refresh'],
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response
