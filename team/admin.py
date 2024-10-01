from django.contrib import admin
from . models import Post,Comment , Team , Member
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Team)
admin.site.register(Member)
