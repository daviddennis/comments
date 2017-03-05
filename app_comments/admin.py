from django.contrib import admin
from app_comments.models import RedditPost, Comment, Increase

# Register your models here.
admin.site.register(RedditPost)
admin.site.register(Comment)
admin.site.register(Increase)
