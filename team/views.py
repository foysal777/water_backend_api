from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post, Comment , Team , Member
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from .permission import isAdminUser, isNormalUser, IsAuthorOrReadOnly
from .serializers import TeamSerializer, MemberSerializer , JoinVolunteerSerializer
from rest_framework import generics
from rest_framework import viewsets
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse


class image_urlView(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)




class PostView(APIView):    
        # ************* 

    def get(self, request, pk=None, format=None):
        if pk:
            post = get_object_or_404(Post, pk=pk)
            serializer = PostSerializer(post)
        else:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)
    
 


    
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):

        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # permission_classes = [isAdminUser]

    def delete(self, request, pk, format=None):

        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentView(APIView):

    def get(self, request, pk=None, format=None):
        # comments = Comment.objects.all()
        if pk:
            comment = get_object_or_404(Comment, pk=pk)
            serializered = CommentSerializer(comment)
            return Response(serializered.data)
        else:
            comments = Comment.objects.all()
            serializered = CommentSerializer(comments, many=True)

        return Response(serializered.data)

    permission_classes = [isAdminUser or isNormalUser]

    def post(self, request, pk=None, format=None):
        serializered = CommentSerializer(data=request.data)
        if serializered.is_valid():
            serializered.save(created_by=request.user)
            return Response(serializered.data, status=status.HTTP_201_CREATED)
        return Response(serializered.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        if pk:
            # Fetch the specific comment to delete
            comment = get_object_or_404(Comment, pk=pk)
            if comment.created_by != request.user:
                return Response({"error": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Comment ID not provided."}, status=status.HTTP_400_BAD_REQUEST)



# Making Team 


class TeamListCreateView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    

class MemberListCreateView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Member.objects.filter(is_pending=True)
        serializer = MemberSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        
        queryset = Member.objects.filter(is_pending=True)
        serializer = MemberSerializer(queryset ,  data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    
    
# only for false request 
class pending_req(APIView):

    def get(self, request, *args, **kwargs):
      
        queryset = Member.objects.filter(is_pending=False)
        serializer = MemberSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        
        queryset = Member.objects.filter(is_pending=False)
        serializer = MemberSerializer(queryset ,  data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
 
    
# Sending Email 


def send_team_email(team_name):
    try:
        team = Team.objects.get(name=team_name)
        print(team)
        members = team.members.all()
        print(members)
        recipient_list = [member.email for member in members]
        print(recipient_list)
        subject = f"Message to {team_name}"
        message = f"Dear {team_name} members, \n\n This is an important message for your team."
        
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Team.DoesNotExist:
        return False
    
    
class SendTeamEmailView(APIView):

    def post(self, request, *args, **kwargs):
        team_name = request.data.get('team_name')
        print(team_name , "hello")
        if send_team_email(team_name):
            
            return Response({"message": "Emails sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
        

# add voluntter or not 


        
        
class AcceptVolunteer(APIView):
    def post(self, request, member_id, *args, **kwargs):
        try:
            member = get_object_or_404(Member, id=member_id)
           
            member.save()
            return Response({'message': f'{member.name} has been accepted to the {member.team.name} team.'}, status=status.HTTP_200_OK)
            

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



# ******************* 
class UpdateMemberStatusAPIView(APIView):
    def patch(self, request, pk, format=None):
        try:
            member = Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MemberSerializer(member, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class JoinVolunteerAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JoinVolunteerSerializer(data=request.data)
        if serializer.is_valid():
            team_id = serializer.validated_data['team_id']
            first_name = serializer.validated_data['first_name']
            email = serializer.validated_data['email']

            # Find the team
            try:
                team = Team.objects.get(id=team_id)
            except Team.DoesNotExist:
                return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)

           
            if Member.objects.filter(team=team, email=email).exists():
                return Response({"error": "User two is already a member of this team."}, status=status.HTTP_400_BAD_REQUEST)

         
            Member.objects.create(
                team=team,
                name=first_name,
                email=email,
                is_pending=False  
            )

            return Response({"success": "Join request sent."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Get request 
    def get(self, request):
        team_id = request.query_params.get('team_id')
        if not team_id:
            return Response({"error": "Team ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Find the team
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)

       
        pending_members = Member.objects.filter(team=team, is_pending=True)
        members_data = [
            {
                "id": member.id,
                "name": member.name,
                "email": member.email,
                "is_pending": member.is_pending,
            }
            for member in pending_members
        ]

        return Response(members_data, status=status.HTTP_200_OK)
    
    
    
    
    
#super user
class IsAdminView(APIView): 
  

    def get(self, request):
        user = request.user
        if user.is_staff:  
            return Response({"is_admin": True})
        return Response({"is_admin": False})    