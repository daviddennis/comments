from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

import requests, json

from app_comments.models import RedditPost, Comment
from annoying.functions import get_object_or_None
from app_comments.lib.comments import CommentBuilder, RedditPostBuilder

class Command(BaseCommand):
    args = ""
    help = ""

    def add_arguments(s, parser):
        pass
        #parser.add_argument('--url', nargs='+', type=str)

    def process_args(s, options):
        pass
        # url = options['url'][0] if options['url'] else None
        # orig_url = url[:]
        # if url:
        #     if url[-5:] != '.json':
        #         url = url[:-1] + '.json'

        # return url, orig_url

    def handle(s, *args, **options):
        Comment.objects.all().delete()
        RedditPost.objects.all().delete()
