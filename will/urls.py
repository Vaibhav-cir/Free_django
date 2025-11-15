from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home, name='home'),
    path('add_Weapon/', views.add_weapon, name='add_weapon'),
    path('edit_weapon/<int:pk>/', views.edit_weapon, name='edit_weapon'),
    path('delete_weapon/<int:pk>/', views.delete_weapon, name='delete_weapon'),
    path('about/', views.about, name="about"),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

]