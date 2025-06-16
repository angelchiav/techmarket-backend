from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, UserProfile, Address, CustomerGroup

User = get_user_model()

class CustomerGroupSerializer(serializers.ModelSerializer):
    """Customer Group Serializer"""

    class Meta:
        model = CustomerGroup
        fields = ['id', 'name', 'description', 'discount_percentage']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    """Extended User Profile Serializer"""

    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'bio', 'website',
            'preferred_language', 'preferred_currency', 'timezone'
        ]
    
    def validate_website(self, value):
        """Only valid websites."""
        if value and not value.startswith('http://', 'https://'):
            raise serializers.ValidationError(
                'The URL starts with http:// o https://'
            )
        return value
    
class AddresSerializer(serializers.ModelSerializer):
    """User Address Serializer"""

    class Meta:
        model = Address
        fields = [
            'id', 'type', 'street_address', 'apartment',
            'city', 'state', 'postal_code', 'country',
            'is_default', 'delivery_instructions',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    """Principal Serializer for Users (READ)"""

    profile = UserProfileSerializer(read_only=True)
    addresses = AddresSerializer(many=True, read_only=True)
    customer_groups = CustomerGroupSerializer(many=True, read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    # Calculated Fields
    total_orders = serializers.SerializerMethodField()
    is_premium_customer = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'birth_date', 'is_verified', 'accepts_marketing',
            'is_active', 'date_joined', 'last_login',
            'profile', 'addresses', 'customer_groups',
            'total_orders', 'is_premium_customer'
        ]
        read_only_fields = [
            'id', 'date_joined', 'last_login', 'is_verified',
            'total_orders', 'is_premium_customer'
        ]
    
    def get_total_orders(self, obj):
        """Total orders of the user"""
        if hasattr(obj, 'orders'):
            return obj.orders.filter(status='completed').status()
        return 0
    
    def get_is_premium_customer(self, obj):
        """If the customer is premium"""
        return obj.orders.filter(name__icontains='premium').exists()
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for the sign up of new users"""

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    # Optional fields on profile.
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    preferred_language = serializers.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'birth_date',
            'accepts_marketing', 'bio', 'preferred_language'
        ]

    def validate_email(self, value):
        """The email is unique"""
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError(
                'The email is already registered.'
            )
        return value.lower()
    
    def validate_username(self, value):
        """The username is unique"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'The username is already taken'
            )
        """Just letters, numbers and underscore"""
        if not value.replace('_', '').isalnum():
            raise serializers.ValidationError(
                'The username can contain only letters, numbers and underscores'
            )
        return value
    
    def validate_phone(self, value):
        """Validating phone number"""
        if value:
            """Removing the space and special characters"""
            clean_phone = ''.join(filter(str.isdigit, value))
            if len(clean_phone) < 10:
                raise serializers.ValidationError(
                    'The phone number has to have at least 10 digits'
                )
            return value
        
    def validate(self, attrs):
        """Validations on object level"""
        # Verifing that the passwords match
        if attrs['password'] != attrs['password']:
            raise ValidationError({
                "password_confirm": "The passwords doesn't match"
            })
        
        #Validating the minimum age
        birth_date = attrs.get('birth_date')
        if birth_date:
            from datetime import date
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 13:
                raise serializers.ValidationError({
                    'birthdate': 'You need to be at least 13 years old to sign up.'
                })
            return attrs
        
        def create(self, validated_data):
            """Creating user with profile"""
            # Removing the fields that doesn't belong to the User model
            password_confirm = validated_data.pop('password_confirm')
            bio = validated_data.pop('bio', '')
            preferred_language = validated_data.pop('preferred_language', 'en')


            # Creating user
            user = User.objects.create_user(**validated_data)

            # Creating profile is data is proportionated
            if bio or preferred_language != 'en':
                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        'bio': bio,
                        'preferred_language': preferred_language
                    }
                )
            return user
class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer to update user info"""

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'birth_date', 
            'accepts_marketing'
        ]
    
    def validate_phone(self, value):
        """Phone validator"""
        if value:
            clean_phone = "".join(filter(str.isdigit, value))
            if len(clean_phone) < 10:
                return serializers.ValidationError(
                    'The phone has to have at least 10 digits'
                )
            return value
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    """Serializer to change the user password"""
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Validating that the password are the same"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
               'new_password_confirm': "The new password does'nt match"
            })
        return attrs
    
class PasswordResetSerializer(serializers.ModelSerializer):
    """Password Reset Request Serializer"""
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Validating that the email exists"""
        try:
            user = User.objects.get(email=value.lower())
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "The email isn't registered in our database"
            )
        return value.lower()

class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    """Password Reset Request"""
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """If the email exists"""
        try:
            user = User.objects.get(email=value.lower())
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "The email is not related with any user"
            )
        return value.lower()

class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    """Confirm Password Reset Request"""

    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )

    new_password_confirm = serializers.CharField(
        required=True,

    )
    
    def validate(self, attrs):
        """Validate that password match"""
        if attrs['new_password'] != attrs['new_passwored_confirm']:
            raise serializers.ValidationError({
                'new password confirm': "The passwords doesn't match"
            })
        return attrs
    
class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    """Reset Password Serializer"""
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Validating that password match"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                ''
            )
    
class UserListSerializer(serializers.ModelSerializer):
    """Simplified Serializer for listing (admin)"""

    full_name = serializers.CharField(source='get_full_name', read_only=True)
    total_orders = serializers.SerializerMethodField()
    last_orders_date = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name',
            'is_active', 'is_verified', 'date_joined',
            'total_orders', 'last_order_date'
        ]
        read_only_files = ['id', 'date_joined']

    def get_total_orders(self, obj):
        """Total orders"""
        if hasattr(obj, 'orders'):
            return obj.orders.count()
        return 0
    
    def get_total_orders_date(self, obj):
        """Last Order Date"""
        if hasattr(obj, 'orders'):
            last_order = obj.orders.order_by('-created_at').first()
            return last_order.created_at if last_order else None
        return None

class UserAdminSerializer(serializers.ModelSerializer):
    """Complete Admin Serializer"""

    profile =  UserProfileSerializer(read_only=True)
    addresses = AddresSerializer(many=True, read_only=True)
    customer_groups = CustomerGroupSerializer(many=True, read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name',
            'last_name', 'full_name', 'phone', 'birth_date',
            'is_active', 'is_superuser', 'is_staff', 'is_verified',
            'accepts_marketing', 'date_joined', 'last_login',
            'last_login_ip', 'profile', 'addresses', 'customer_groups'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'last_login_ip']

        def update(self, instance, validated_data):
            """Update with additional validations for admin"""
            # Only superusers can change is_staff and is_admin
            request = self.context.get('request')
            if request and not request.user.is_superuser:
                validated_data.pop('is_staff', None)
                validated_data.pop('is_superuser', None)

            return super().update(instance, validated_data)
        
# Serializer for custom JWT
class CustomTokenObtainPairSerializer(serializers.Serializer):
    """Custom Serializer for login"""

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        """Validate credentials"""
        from django.contrib.auth import authenticate

        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username = email,
                password = password
            )
            if not user:
                raise serializers.ValidationError(
                    'This email is not registered'
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    'The email is not enabled'
                )
            
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError(
            'Fill the obligatory fields'
        )