from django.urls import path
from . import views
from . import api_views  # Import the API views
from django.contrib.auth import views as auth_views
from .views import logout_view, register_view
from django.contrib.auth import views as auth_views
from .views import Home
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from shop.views import protected_view
from .views import custom_login, logout_view
from .views import custom_login_view , about_view
from django.urls import path
from .views import CustomTokenObtainPairView, LogoutView, RevokeTokenView, JWTLoginView, protected_view, RegisterView


urlpatterns = [
    # path('', views.home, name='home'),
    path('api/products/', views.ProductListView.as_view(), name='product_list_api'),
    path('', views.product_list, name='product_list'),  # Root URL for the product list
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'), 
    path('', views.product_list, name='product_list'),
    path('login/', JWTLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/protected/', protected_view, name='protected_view'),
    path('search/', views.search, name='search'),
    path('product/image/upload/', views.product_image_upload, name='product_image_upload'),
    path('api/products/', api_views.ProductList.as_view(), name='product_list_api'),  # API URL for product list
    path('api/products/<int:pk>/', api_views.ProductDetail.as_view(), name='product_detail_api'),  # API URL for product detail
    path('api/categories/', api_views.CategoryList.as_view(), name='category_list_api'),  # API URL for category list
    path('api/categories/<int:pk>/', api_views.CategoryDetail.as_view(), name='category_detail_api'),  # API URL for category detail
    path('', Home.as_view()),
    path('about/', about_view, name='about'),
    path('api/protected/', protected_view, name='protected_view'),
    path('api/login/', custom_login_view, name='custom_login'),
    path('api/token/revoke/', RevokeTokenView.as_view(), name='token_revoke'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', custom_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
              ]



