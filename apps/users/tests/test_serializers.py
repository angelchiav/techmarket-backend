# apps/users/tests/test_serializers.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.users.serializers import (
    UserSerializer, 
    UserRegistrationSerializer,
    ChangePasswordSerializer,
    AddressSerializer
)

User = get_user_model()

class UserSerializerTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
    
    def test_user_serializer_data(self):
        """Test de serialización de usuario"""
        serializer = UserSerializer(self.user)
        data = serializer.data
        
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['full_name'], 'Test User')
        self.assertIn('id', data)
        self.assertNotIn('password', data)  # Password no debe aparecer

class UserRegistrationSerializerTest(TestCase):
    
    def test_valid_registration_data(self):
        """Test de registro con datos válidos"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'strongpass123',
            'password_confirm': 'strongpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.email, 'new@example.com')
        self.assertTrue(user.check_password('strongpass123'))
    
    def test_password_mismatch(self):
        """Test de error cuando las contraseñas no coinciden"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'strongpass123',
            'password_confirm': 'differentpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password_confirm', serializer.errors)
    
    def test_duplicate_email(self):
        """Test de error con email duplicado"""
        # Crear usuario existente
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='pass123'
        )
        
        # Intentar registrar con mismo email
        data = {
            'username': 'newuser',
            'email': 'existing@example.com',  # Email duplicado
            'password': 'strongpass123',
            'password_confirm': 'strongpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

class ChangePasswordSerializerTest(TestCase):
    
    def test_valid_password_change(self):
        """Test de cambio de contraseña válido"""
        data = {
            'old_password': 'oldpass123',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123'
        }
        
        serializer = ChangePasswordSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_password_confirm_mismatch(self):
        """Test de error cuando las nuevas contraseñas no coinciden"""
        data = {
            'old_password': 'oldpass123',
            'new_password': 'newpass123',
            'new_password_confirm': 'differentpass123'
        }
        
        serializer = ChangePasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_password_confirm', serializer.errors)