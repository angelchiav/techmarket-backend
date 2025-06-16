# apps/users/tests/test_api.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserAPITestCase(APITestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.client = APIClient()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Crear superusuario
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # URLs
        self.register_url = reverse('users:user-register')
        self.login_url = reverse('token_obtain_pair')
        self.me_url = reverse('users:user-me')
        self.change_password_url = reverse('users:change-password')
    
    def test_user_registration(self):
        """Test de registro de usuario"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'strongpass123',
            'password_confirm': 'strongpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'new@example.com')
        
        # Verificar que el usuario se creó en la BD
        self.assertTrue(User.objects.filter(email='new@example.com').exists())
    
    def test_user_login(self):
        """Test de login"""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_get_user_profile_authenticated(self):
        """Test de obtener perfil de usuario autenticado"""
        # Autenticar usuario
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['id'], self.user.id)
    
    def test_get_user_profile_unauthenticated(self):
        """Test de obtener perfil sin autenticación"""
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_user_profile(self):
        """Test de actualización de perfil"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone': '+1234567890'
        }
        
        response = self.client.patch(self.me_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        
        # Verificar en BD
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
    
    def test_change_password(self):
        """Test de cambio de contraseña"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123'
        }
        
        response = self.client.post(self.change_password_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que la contraseña cambió
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123'))
    
    def test_change_password_wrong_old_password(self):
        """Test de cambio de contraseña con contraseña actual incorrecta"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'old_password': 'wrongpass',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123'
        }
        
        response = self.client.post(self.change_password_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old_password', response.data)

class AddressAPITestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.addresses_url = reverse('users:address-list')
    
    def test_create_address(self):
        """Test de creación de dirección"""
        data = {
            'type': 'shipping',
            'street_address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'postal_code': '12345',
            'country': 'Test Country'
        }
        
        response = self.client.post(self.addresses_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['street_address'], '123 Test St')
        
        # Verificar en BD
        from apps.users.models import Address
        self.assertTrue(Address.objects.filter(user=self.user, city='Test City').exists())
    
    def test_list_user_addresses(self):
        """Test de listar direcciones del usuario"""
        # Crear direcciones de prueba
        from apps.users.models import Address
        Address.objects.create(
            user=self.user,
            type='shipping',
            street_address='123 Test St',
            city='Test City',
            postal_code='12345',
            country='Test Country'
        )
        
        response = self.client.get(self.addresses_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['city'], 'Test City')
    
    def test_user_can_only_see_own_addresses(self):
        """Test que usuarios solo ven sus propias direcciones"""
        # Crear otro usuario con dirección
        other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='pass123'
        )
        
        from apps.users.models import Address
        Address.objects.create(
            user=other_user,
            type='shipping',
            street_address='456 Other St',
            city='Other City',
            postal_code='67890',
            country='Other Country'
        )
        
        response = self.client.get(self.addresses_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No debe ver direcciones de otros