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
        parser.add_argument('--url', nargs='+', type=str)

    def process_args(s, options):
        url = options['url'][0] if options['url'] else None
        orig_url = url[:]
        if url:
            if url[-5:] != '.json':
                url = url[:-1] + '.json'

        return url, orig_url

    def handle(s, *args, **options):
        url, orig_url = s.process_args(options)

        existing_data = get_object_or_None(RedditPost, url=url)
        if existing_data:
            print('Found from DB.\n\n')
            text_json = existing_data
        else:
            # http
            print('Getting by http: %s' % url)
            resp = requests.get(url)
            if resp.status_code == 200:
                received_text = resp.text
                #print(received_text[:5])
            else:
                print(resp.text)
                print('Reading from file...')
                with open('comment.json') as fp:
                    received_text = fp.read()
                #return
            if not received_text:
                print('No text gotten')
            text_json = received_text

        if not text_json:
            raise Exception('No JSON text found')

        comment_json = json.loads(text_json)

        comment_section = RedditPostBuilder(orig_url, comment_json)

