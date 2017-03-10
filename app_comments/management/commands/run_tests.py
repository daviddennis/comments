from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from app_comments.lib.comments import PostGetter
from app_comments.lib.util import get_basic_link, get_json_link
from app_comments.models import RedditPost


class Command(BaseCommand):
    args = ""
    help = ""

    def add_arguments(self, parser):
        pass
        #parser.add_argument('--url', nargs='+', type=str)

    def process_args(self, options):
        pass

    def handle(self, *args, **options):
        self.url1 = 'https://www.reddit.com/r/Futurology/comments/5yk8yt/epilepsy_patients_turning_to_medicinal_cannabis/?utm_content=comments&utm_medium=hot&utm_source=reddit&utm_name=Futurology'

        # self.test_get_basic_link()
        # self.test_get_json_link()
        self.test_post_getter()

    def test_get_basic_link(self):
        basic_url = get_basic_link(self.url1)
        print(basic_url)
        assert basic_url is not None

    def test_get_json_link(self):
        json_link = get_json_link(self.url1)
        print(json_link)

    def test_post_getter(self):
        pg = PostGetter()
        pg.get(self.url1)
