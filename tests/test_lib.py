from annoying.functions import get_object_or_None

from app_comments.lib.comments import PostGetter
from app_comments.lib.util import get_basic_link
from app_comments.models import RedditPost

from django.test import TestCase


class UtilTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_basic_link(self):
        url = 'https://www.reddit.com/r/Futurology/comments/5yk8yt/epilepsy_patients_turning_to_medicinal_cannabis/?utm_content=comments&utm_medium=hot&utm_source=reddit&utm_name=Futurology'

        basic_url = get_basic_link(url)
        print(basic_url)
        assert True

# class PostGetterTestCase(TestCase):
#     def setUp(self):
#         self.pg = PostGetter()

#     def test_post_already_exists(self):
#         reddit_post = RedditPost.objects.all()[0]
#         self.pg.get(reddit_post.url, reddit_post.url)
#         #resp = pg.get(json_url, json_url)