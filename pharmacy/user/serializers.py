from rest_framework import serializers
from .models import CustomUser, AdminProfile
from pharma.models import Pharmacy


class CustomUserSerializer(serializers.ModelSerializer):

    pharmacy = serializers.PrimaryKeyRelatedField(queryset=Pharmacy.objects.all()) #name of the pharmacy from the __str__ function

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'pharmacy', 'contact_number', 'user_address']
        read_only_fields = ['id']  

class AdminProfileSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer()
    working_at = serializers.StringRelatedField() 

    class Meta:
        model = AdminProfile
        fields = ['id', 'user', 'working_at', 'shift', 'salary']
        read_only_fields = ['id']  

    def create(self, validated_data):
        
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create(**user_data) 
        #The **user_data syntax unpacks the user_data dictionary 
        #and passes the key-value pairs as arguments to the CustomUser.objects.create() method
        admin_profile = AdminProfile.objects.create(user=user, **validated_data) 
        return admin_profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data: #if there's any data related to the user fields, make the updates
            instance.user.username = user_data.get('username', instance.user.username)
            instance.user.email = user_data.get('email', instance.user.email)
            instance.user.contact_number = user_data.get('contact_number', instance.user.contact_number)
            instance.user.user_address = user_data.get('user_address', instance.user.user_address)
            instance.user.save()
        
        instance.working_at = validated_data.get('working_at', instance.working_at)
        instance.shift = validated_data.get('shift', instance.shift)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.save()
        return instance
