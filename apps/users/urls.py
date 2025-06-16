from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListView.as_view(), name='user-list'),
    path('me/', views.UserMeView.as_view(), name='user-me'),
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('addresses/', views.AddressListView.as_view(), name='address-list'),
    path('addresses/<int:pk>/', views.AddressDetailView.as_view(), name='address-detail'),
    path('addresses/<int:pk>/set-default/', views.SetDefaultAddressView.as_view(), name='set-default-address'),
] 