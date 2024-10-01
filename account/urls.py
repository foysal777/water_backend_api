from django.urls import path, include
# from .views import 
from . import views  




urlpatterns = [
    path('register/', views.userRegistration.as_view() , name= 'register'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('api/user-role/', views.UserRoleView.as_view(), name='user-role'), 
]