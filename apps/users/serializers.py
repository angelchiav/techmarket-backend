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
        fields = ['avatar', 'bio', 'website']
    
    def validate_website(self, value):
        """Only valid websites."""
        if value and not (value.startswith('http://') or value.startswith('https://')):
            raise serializers.ValidationError(
                'The URL must start with http:// or https://'
            )
        return value

class AddressSerializer(serializers.ModelSerializer):
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
    addresses = AddressSerializer(many=True, read_only=True)
    customer_groups = CustomerGroupSerializer(many=True, read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone', 'birth_date', 'address', 'is_verified',
            'accepts_marketing', 'profile', 'addresses',
            'customer_groups', 'full_name'
        ]
        read_only_fields = ['id', 'email', 'is_verified']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for the sign up of new users"""
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'birth_date',
            'accepts_marketing', 'profile'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

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
        if not value.replace('_', '').isalnum():
            raise serializers.ValidationError(
                'The username can contain only letters, numbers and underscores'
            )
        return value
    
    def validate_phone(self, value):
        """Validating phone number"""
        if value:
            clean_phone = ''.join(filter(str.isdigit, value))
            if len(clean_phone) < 10:
                raise serializers.ValidationError(
                    'The phone number has to have at least 10 digits'
                )
            return value
        return value
        
    def validate(self, data):
        """Validations on object level"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': "The passwords don't match"
            })
        
        birth_date = data.get('birth_date')
        if birth_date:
            from datetime import date
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 13:
                raise serializers.ValidationError({
                    'birth_date': 'You need to be at least 13 years old to sign up.'
                })
        return data

    def create(self, validated_data):
        """Creating user with profile"""
        profile_data = validated_data.pop('profile', {})
        password_confirm = validated_data.pop('password_confirm')
        
        # Creating user
        user = User.objects.create_user(**validated_data)

        # Creating profile if data is provided
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        else:
            UserProfile.objects.create(user=user)

        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer to update user info"""
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'birth_date', 
            'accepts_marketing', 'profile'
        ]
    
    def validate_phone(self, value):
        """Phone validator"""
        if value:
            clean_phone = "".join(filter(str.isdigit, value))
            if len(clean_phone) < 10:
                raise serializers.ValidationError(
                    'The phone has to have at least 10 digits'
                )
            return value
        return value

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # Update User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Profile fields
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer to change the user password"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        """Validating that the passwords are the same"""
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': "The new passwords don't match"
            })
        return data

class UserListSerializer(serializers.ModelSerializer):
    """Simplified Serializer for listing (admin)"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    total_orders = serializers.SerializerMethodField()
    last_order_date = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name',
            'is_active', 'is_verified', 'date_joined',
            'total_orders', 'last_order_date'
        ]
        read_only_fields = ['id', 'date_joined']

    def get_total_orders(self, obj):
        """Total orders of the user"""
        if hasattr(obj, 'orders'):
            return obj.orders.filter(status='completed').count()
        return 0

    def get_last_order_date(self, obj):
        """Last order date"""
        if hasattr(obj, 'orders'):
            last_order = obj.orders.order_by('-created_at').first()
            return last_order.created_at if last_order else None
        return None

class UserAdminSerializer(serializers.ModelSerializer):
    """Complete Admin Serializer"""
    profile = UserProfileSerializer(read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)
    customer_groups = CustomerGroupSerializer(many=True, read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name',
            'last_name', 'full_name', 'phone', 'birth_date',
            'is_active', 'is_superuser', 'is_staff', 'is_verified',
            'accepts_marketing', 'date_joined', 'last_login',
            'profile', 'addresses', 'customer_groups'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']

    def update(self, instance, validated_data):
        """Update user and related data"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance