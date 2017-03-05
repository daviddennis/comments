from annoying.functions import get_object_or_None

from django.shortcuts import render
from django.http import HttpResponse, Http404

from app_comments.models import Increase, RedditPost
from app_comments.lib.comments import PostGetter, dfs
from app_comments.lib.util import get_json_link


def index(request):

    context = {}

    inc_exclude_filter = {
        'child_comment__body__startswith': '[removed]',
        'child_comment__body__startswith': '[deleted]',
        'parent_comment__body__startswith': '[removed]',
        'parent_comment__body__startswith': '[deleted]',
    }

    all_increases = Increase.objects.exclude(**inc_exclude_filter).order_by('-percent').all()
    # for inc in all_increases:
    context['increases'] = all_increases

    return render(request, 'app_comments/index.html', context)


def get_link(request):
    url = request.GET.get('link')

    if not 'http' in url:
        raise Exception('Not a url')

    json_url = get_json_link(url)

    reddit_post = get_object_or_None(RedditPost, url=json_url)

    if not reddit_post:
        pg = PostGetter()
        resp = pg.get(json_url, json_url)

        if not resp:
            raise Http404('Not loaded correctly')

    dfs(reddit_post, 0, post=reddit_post)
    increases = Increase.objects.filter(reddit_post__url=reddit_post.url).\
        order_by('-percent').\
        all()

    context = {
        'increases': increases,
    }

    return render(request, 'app_comments/specific_link.html', context)
