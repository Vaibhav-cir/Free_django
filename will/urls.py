from django.urls import path
from .views import (
    HomeView,
    CustomLoginView,
    RegisterView,
    CustomLogoutView,
    WeaponCreateView,
    WeaponUpdateView,
    WeaponDeleteView,
    AboutView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('add_weapon/', WeaponCreateView.as_view(), name='add_weapon'),
    path('edit_weapon/<int:pk>/', WeaponUpdateView.as_view(), name='edit_weapon'),
    path('delete_weapon/<int:pk>/', WeaponDeleteView.as_view(), name='delete_weapon'),
    path('about/', AboutView.as_view(), name='about'),
]