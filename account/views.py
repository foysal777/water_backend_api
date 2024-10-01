from django.shortcuts import render,redirect
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.views import APIView
from  . import serializers
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import CustomUser

from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerialization , UserLoginSerializer  , CustomUserSerializer

# Create your views here.


class UserRoleView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)  
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class userRegistration(APIView):       
    serializer_class = RegistrationSerialization
       
    def post(self, request):
        serializer = self.serializer_class(data=request.data)          
        if serializer.is_valid():
            user =  serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            print(token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid" , uid)
            confirm_link = f"https://water-backend-d44x.onrender.com/account/active/{uid}/{token}/"
            email_subject = "Confirm Your Email Now"
            email_body = render_to_string('confirm_email.html', { 'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject , "" , to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            
            return Response({"Check Your E-mail Confirmation.."}, status=status.HTTP_201_CREATED)
            
        return Response (serializer.errors , status=status.HTTP_400_BAD_REQUEST)
 
 
 
def activate(request, uid64, token): 
    print(uid64)
    print(token)
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(CustomUser.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
     
        user.is_active = True  
        user.save()
        return redirect('https://foysal777.github.io/water_logging_fronted/login.html')
    else:
        return redirect('register')
    
  
    
# log in part 
class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id})
            else:
                return Response({'error' : "Invalid Credential"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
#  log out part 


class UserLogoutView(APIView):
    def get(self, request):
        if request.user.is_authenticated:       
            Token.objects.filter(user=request.user).delete()                     
            logout(request)     
            return redirect('login')
        else:     
            return redirect('login')  
            

      
