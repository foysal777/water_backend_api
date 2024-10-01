from django.urls import path ,include
from .views import PostView , CommentView 
from rest_framework.routers import DefaultRouter
from .views import image_urlView ,TeamListCreateView, IsAdminView , JoinVolunteerAPIView, pending_req ,MemberListCreateView , UpdateMemberStatusAPIView, SendTeamEmailView   , AcceptVolunteer 


router = DefaultRouter()
router.register('imgurl/', image_urlView)

urlpatterns = [
    path('', include(router.urls)),
    path('post/', PostView.as_view(), name='post-list'),  
    path('post/<int:pk>/', PostView.as_view(), name='post-detail'),  
    path('comment/', CommentView.as_view(), name='comment_all'),  
    path('comment/<int:pk>/', CommentView.as_view(), name='comments'), 
    path('teams/', TeamListCreateView.as_view(), name='team-list-create'),
    path('members/', MemberListCreateView.as_view(), name='member-list-create'),
    path('pending_request/', pending_req.as_view(), name='pending_request'),
    path('send-team-email/', SendTeamEmailView.as_view(), name='send_team_email'),
    path('team/accept-volunteer/<int:member_id>/', AcceptVolunteer.as_view(), name='accept_volunteer'),
    path('members/<int:pk>/update-status/', UpdateMemberStatusAPIView.as_view(), name='update-member-status'),
    path('join-volunteer/', JoinVolunteerAPIView.as_view(), name='join-volunteer'),
    path('is_admin/', IsAdminView.as_view(), name='is_admin')

  
]