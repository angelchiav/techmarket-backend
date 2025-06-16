# apps/users/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from apps.users.models import CustomerGroup, Address

User = get_user_model()

class UserModelTest(TestCase):
    
    def setUp(self):
        """Configuración que se ejecuta antes de cada test"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123'
        }
    
    def test_create_user(self):
        """Test de creación de usuario"""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_verified)
        self.assertFalse(user.is_staff)
    
    def test_create_superuser(self):
        """Test de creación de superusuario"""
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_user_string_representation(self):
        """Test del método __str__"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'test@example.com')
    
    def test_email_unique(self):
        """Test que el email debe ser único"""
        User.objects.create_user(**self.user_data)
        
        # Intentar crear otro usuario con el mismo email
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                email='test@example.com',  # Email duplicado
                password='testpass123'
            )
    
    def test_user_full_name(self):
        """Test del nombre completo"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_full_name(), 'Test User')

class CustomerGroupModelTest(TestCase):
    
    def test_create_customer_group(self):
        """Test de creación de grupo de clientes"""
        group = CustomerGroup.objects.create(
            name='Premium',
            description='Clientes premium',
            discount_percentage=10.00,
            min_orders=5,
            min_spent=100.00
        )
        
        self.assertEqual(group.name, 'Premium')
        self.assertEqual(group.discount_percentage, 10.00)
        self.assertTrue(group.is_active)
    
    def test_customer_group_string_representation(self):
        """Test del método __str__"""
        group = CustomerGroup.objects.create(name='VIP')
        self.assertEqual(str(group), 'VIP')

class AddressModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_address(self):
        """Test de creación de dirección"""
        address = Address.objects.create(
            user=self.user,
            type='shipping',
            street_address='123 Test St',
            city='Test City',
            state='Test State',
            postal_code='12345',
            country='Test Country'
        )
        
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.city, 'Test City')
        self.assertFalse(address.is_default)
    
    def test_set_default_address(self):
        """Test de dirección por defecto"""
        # Crear primera dirección como default
        address1 = Address.objects.create(
            user=self.user,
            type='shipping',
            street_address='123 Test St',
            city='Test City',
            postal_code='12345',
            country='Test Country',
            is_default=True
        )
        
        # Crear segunda dirección como default
        address2 = Address.objects.create(
            user=self.user,
            type='shipping',
            street_address='456 Another St',
            city='Another City',
            postal_code='67890',
            country='Test Country',
            is_default=True
        )
        
        # Refrescar desde BD
        address1.refresh_from_db()
        
        # Solo address2 debe ser default
        self.assertFalse(address1.is_default)
        self.assertTrue(address2.is_default)