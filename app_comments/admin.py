from django.contrib import admin
from app_comments.models import RedditPost, Comment

# Register your models here.
admin.site.register(RedditPost)
admin.site.register(Comment)
