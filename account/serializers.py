from rest_framework import serializers
from .models import CustomUser

# user authenticated part 
class RegistrationSerialization(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = CustomUser   
        fields = ['username' , 'first_name' ,'last_name' , 'email' , 'password' ,  'confirm_password']
        
    
    def save(self):
        # role = self.validated_data['role']
  
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
       
        if password != password2:
            raise serializers.ValidationError({'error' : "Password Doesn't Match"})
        
        if CustomUser.objects.filter(email = email).exists():
            raise serializers.ValidationError({'error' : "Email Already Exists."})   
        
        
        # if role == 'volunteer_user':
        #     print(role)
        #     member = Member.objects.filter(members__email=email)
        #     if not member.exists():
        #         raise serializers.ValidationError({'error': "Only team members can register as Volunteer User."})   
        
        account = CustomUser(username = username , email = email , first_name = first_name , last_name = last_name )
        account.set_password(password)
        account.is_active = False  #confirmation link deye active korbo tai 
        account.save()
        return account
    
    


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)     
    
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role' ,'first_name']