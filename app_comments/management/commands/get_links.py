from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

import requests, json

from app_comments.models import RedditPost, Comment
from annoying.functions import get_object_or_None
from app_comments.lib.comments import CommentBuilder, RedditPostBuilder
from bs4 import BeautifulSoup
from app_comments.management.commands.get_comments import PostGetter
from time import sleep


class Command(BaseCommand):
    args = ""
    help = ""

    def add_arguments(s, parser):
        parser.add_argument('--url', nargs='+', type=str)

    def process_args(s, options):
        url = options['url'][0] if options['url'] else None
        return url
        # orig_url = url[:]
        # if url:
        #     if url[-5:] != '.json':
        #         url = url[:-1] + '.json'

        # return url, orig_url

    def handle(s, *args, **options):
        #url = s.process_args(options)
        #print(url)
        url = 'https://www.reddit.com/top.json?sort=top&t=year'
        base_url = 'https://www.reddit.com'
        resp = requests.get(url)
        if resp.status_code == 200:
            text_json = resp.text
        else:
            print(resp.text)
            return

        page_json = json.loads(text_json)

        for post_info in page_json['data']['children']:
            comments_url = base_url + post_info['data']['permalink']
            comments_json_url = comments_url[:-1]+'.json'
            pg = PostGetter()
            resp = pg.get(comments_json_url, comments_url)
            print(resp, 1)
            if resp == 'bad http':
                sleep_time = 5
                print('sleeping (%s)...' % sleep_time)
                sleep(sleep_time)
                resp = pg.get(comments_json_url, comments_url)
                if resp == 'bad http':
                    print('sleeping (%s)...' % sleep_time)
                    sleep(sleep_time)
                    resp = pg.get(comments_json_url, comments_url)
                    if resp == 'bad http':
                        print('sleeping (%s)...' % sleep_time)
                        sleep(sleep_time)
            # cmd_data = {'--url': comments_url}
            # call_command('get_comments', **cmd_data)
            # break
