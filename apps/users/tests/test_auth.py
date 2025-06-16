# apps/users/tests/test_auth.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

User = get_user_model()

class AuthenticationTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
    
    def test_jwt_token_generation(self):
        """Test de generación de tokens JWT"""
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        
        self.assertIsNotNone(str(refresh))
        self.assertIsNotNone(str(access))
    
    def test_protected_endpoint_without_token(self):
        """Test de acceso a endpoint protegido sin token"""
        url = reverse('users:user-me')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_protected_endpoint_with_token(self):
        """Test de acceso a endpoint protegido con token"""
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        
        url = reverse('users:user-me')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_token(self):
        """Test con token inválido"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        
        url = reverse('users:user-me')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PermissionsTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='pass123'
        )
        
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='pass123'
        )
        
        self.client = APIClient()
    
    def test_admin_can_list_all_users(self):
        """Test que admin puede listar todos los usuarios"""
        self.client.force_authenticate(user=self.admin)
        
        url = reverse('users:user-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_regular_user_cannot_list_all_users(self):
        """Test que usuario regular no puede listar todos los usuarios"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('users:user-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)