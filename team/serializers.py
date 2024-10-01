from rest_framework import serializers
from .models import Post , Comment, Member , Team , Volunteer
from .utils import upload_image_to_imgbb 


class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'location' , 'image','image_url' ,'created_at', 'role' ]
        read_only_fields=['id']
        
    def create(self, validated_data):
        image_file = validated_data.pop('image_file', None)
        if image_file:
            image_url = upload_image_to_imgbb(image_file)
            if image_url:
                validated_data['image_url'] = image_url
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
        



        
class MemberSerializer(serializers.ModelSerializer):
    
    team = serializers.StringRelatedField()
    class Meta:
        
        model = Member
        fields = ['id', 'name', 'team' , 'contact_number' ,'email'  , 'is_pending' , 'role'  ]
        
    def update(self, instance, validated_data):
        is_pending = validated_data.get('is_pending', instance.is_pending)

     
        if is_pending and not instance.is_pending:
    
            instance.user.role = 'volunteer_team'
             
            instance.user.save()


        instance.is_pending = is_pending
        instance.save()

        return instance  
  


class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        
        model = Team
        fields = ['id', 'name',  'members']        




class JoinVolunteerSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Volunteer
        fields= ['team_id' , 'first_name' , 'email']
   