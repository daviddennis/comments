import json
import sys
import requests
from app_comments.lib.util import Printer, get_basic_link, get_json_link
from app_comments.models import Comment, RedditPost, Increase
from annoying.functions import get_object_or_None


class CommentBuilder(Printer):

    def __init__(s, data, reddit_post=None, parent_comment=None):
        s.visited = False

        s.data = data

        s._id = None
        s.body = None
        s.score = None
        s.reddit_post = reddit_post
        s.parent_comment = parent_comment
        s.is_reference = False

        s._id = data['id']
        s.name = data.get('name')
        s.reddit_parent_id = data.get('parent_id')
        s.body = data['body'].replace('\n', '\n\t\t')
        s.score = int(data['score'])

    def build(s):
        comment = get_object_or_None(Comment, _id=s._id)
        if comment:
            return comment

        comment = Comment(body=s.body, score=s.score, _id=s._id, visited=s.visited,
                          reddit_post=s.reddit_post, parent=s.parent_comment,
                          name=s.name)
        comment.save()

        if s.data.get('replies') and isinstance(s.data['replies'], dict):
            for j in s.data['replies']['data']['children']:
                if j['kind'] != 'more':
                    cb = CommentBuilder(j['data'], reddit_post=s.reddit_post, parent_comment=comment)
                    child_comment = cb.build()
                    comment.children.add(child_comment)

        return comment


class RedditPostBuilder(Printer):

    def __init__(s, url, data):
        s.visited = False
        s.body = 'STUB'
        s.score = None

        s.data = data

        s.url = url

        post_data = data[0]['data']['children'][0]['data']
        # print(post_data)
        s.title = post_data['title']
        s._id = post_data['id']

    def build(s):
        existing_rp = reddit_post = get_object_or_None(RedditPost, _id=s._id)
        if not reddit_post:
            reddit_post = RedditPost(_id=s._id, visited=s.visited, url=s.url, title=s.title, json_data=json.dumps(s.data))
            reddit_post.save()

        for j in s.data[1]['data']['children'][:-1]:
            if j.get('data'):
                cb = CommentBuilder(j['data'], reddit_post=reddit_post)
                new_comment = cb.build()

        return reddit_post

# def get_post(url):
#     if not url:
#         raise Exception('!')
#     basic_url = get_basic_link(url)
#     if not basic_url:
#         raise Exception('!')
#     reddit_post = get_object_or_None(RedditPost, url=orig_url)
#     if reddit_post:


class PostGetter:

    def build_reddit_post(self, url, json_text, reddit_post=None):
        comment_json = json.loads(json_text)
        if not reddit_post or (reddit_post and not reddit_post.loaded):
            rpb = RedditPostBuilder(url, comment_json)
            reddit_post = rpb.build()
            reddit_post.loaded = True
            reddit_post.save()
            print('Post loaded.')
            return reddit_post

    def get(self, url):
        basic_url = get_basic_link(url)
        reddit_post = get_object_or_None(RedditPost, url=basic_url)
        if reddit_post:
            print('Found from DB.')
            return reddit_post
            # if not reddit_post.json_data
            # return self.build_reddit_post(basic_url,
            #                               reddit_post,
            #                               reddit_post.json_data)
        else:
            json_link = get_json_link(basic_url)
            print('Getting by http: %s' % json_link)
            json_text = self.get_by_http(json_link)
            print(json_text[:200])
            return self.build_reddit_post(basic_url,
                                          json_text)

    def get_by_http(self, url):
        resp = requests.get(url)
        if resp.status_code == 200:
            json_text = resp.text
            #print(received_text[:5])
        else:
            print(resp.text)
            raise Exception('bad http')

        if not json_text:
            raise Exception('No JSON text found')

        return json_text

        # print(resp.text)
        # print('Reading from file...')
        # with open('comment.json') as fp:
        #     received_text = fp.read()


# class PostGetter:

#     def get(s, url, orig_url):
#         reddit_post = get_object_or_None(RedditPost, url=orig_url)
#         if reddit_post:
#             print('Found from DB.\n\n')
#             text_json = reddit_post.json_data
#         else:
#             # http
#             print('Getting by http: %s' % url)
#             resp = requests.get(url)
#             if resp.status_code == 200:
#                 received_text = resp.text
#                 #print(received_text[:5])
#             else:
#                 # print(resp.text)
#                 # print('Reading from file...')
#                 # with open('comment.json') as fp:
#                 #     received_text = fp.read()
#                 print(resp.text)
#                 return 'bad http'
#             if not received_text:
#                 print('No text gotten')
#             text_json = received_text

#         if not text_json:
#             raise Exception('No JSON text found')

#         #print(text_json, '>>')

#         comment_json = json.loads(text_json)

#         if (reddit_post and not reddit_post.loaded) or reddit_post is None:
#             rpb = RedditPostBuilder(orig_url, comment_json)
#             reddit_post = rpb.build()
#             reddit_post.loaded = True
#             reddit_post.save()
#             print('Post loaded.')
#             return reddit_post


def dfs(node, count, parent=None, limit=100, post=None):
    if count >= 11:
        return

    if not node:
        return

    node.visited = True

    if parent and parent.score and node.score:
        if parent.score < node.score:
            pct = int((node.score/float(parent.score)*100) - 100)
            if pct > limit:

                incr_data = {'parent_comment': parent,
                             'child_comment': node,
                             'percent': pct,
                             'reddit_post': post}

                if not Increase.objects.filter(**incr_data).all():
                    # record
                    new_increase = Increase(**incr_data)
                    new_increase.save()

    for c in node.children.all():
        if not c.visited:
            dfs(c, count+1, parent=node, post=post)
