import json, sys
from app_comments.lib.util import Printer
from app_comments.models import Comment, RedditPost
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
