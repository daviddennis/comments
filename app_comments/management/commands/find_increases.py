from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

import requests
import json

from app_comments.models import RedditPost, Comment, Increase
from app_comments.lib.comments import dfs
from annoying.functions import get_object_or_None


class Command(BaseCommand):
    args = ""
    help = ""

    def add_arguments(s, parser):
        parser.add_argument('--url', nargs='+', type=str)

    def process_args(s, options):
        url = options['url'][0] if options['url'] else None
        orig_url = None
        if url:
            orig_url = url[:]
            if url:
                if url[-5:] != '.json':
                    url = url[:-1] + '.json'

        return url, orig_url

    def handle(s, *args, **options):
        url, orig_url = s.process_args(options)

        #reddit_post = get_object_or_None(RedditPost, url=orig_url)

        # if not reddit_post:
        #     raise

        # s.limit = 100  # if not limit else limit

        for reddit_post in RedditPost.objects.all():
            dfs(reddit_post, 0)
