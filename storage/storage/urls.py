from captcha.views import captcha_refresh
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from django.urls import include
from sklad import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view,name='login'),
    path('storage/', views.storage_view, name='storage'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('users/create/', views.user_create, name='user_create'),


]


