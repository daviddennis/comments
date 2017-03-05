# from django.core.management import call_command
from django.core.management.base import BaseCommand

from app_comments.lib.comments import PostGetter
from app_comments.lib.util import get_json_link


class Command(BaseCommand):
    args = ""
    help = ""

    def add_arguments(s, parser):
        parser.add_argument('--url', nargs='+', type=str)

    def process_args(s, options):
        url = options['url'][0] if options['url'] else None
        orig_url = url[:]

        url = get_json_link(url)
        return url, orig_url

    def handle(s, *args, **options):
        url, orig_url = s.process_args(options)

        pg = PostGetter()
        pg.get(url, orig_url)

        #print('Already loaded.')

        # c = Comment.objects.filter(_id='dbnr8tc').all()[0]
        # print(c.name)
        # print(c.children.all())

        # if not reddit_post.visited:
