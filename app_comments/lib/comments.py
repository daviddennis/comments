import json
from app_comments.lib.util import Printer
from app_comments.models import Comment


class CommentBuilder(Printer):

    def __init__(s, data):
        s.visited = False

        s.data = data

        s._id = None
        s.body = None
        s.score = None

        if not data.get('body'): ### fix
            s.children = []
            return

        if data.get('replies') and isinstance(data['replies'], dict):
            s._id = data['id']
            s.body = data['body'].replace('\n', '\n\t\t')
            s.score = int(data['score'])
        else:
            s.children = []

        return s.build(data)

    def build(s, data):

        new_comment = Comment(body=s.body, score=s.score, _id=s._id, visited=s.visited)
        new_comment.save()

        for j in data['replies']['data']['children']:
            CommentBuilder(j['data'])
        #new_comment.children = [ for j in]

        return new_comment
        # for child_comment in s.children:
        #     new_comment.children.add(child_comment)

    # def x(s):
    #     print(s.children[0].children[0].body)


class RedditPostBuilder(Printer):

    def __init__(s, url, data):
        s.visited = False
        s.body = 'STUB'
        s.score = None

        s.url = url

        post_data = data[0]['data']
        print(post_data)
        s.title = post_data['title']
        s._id = post_data['id']

        return s.build(data)

    def build(s, data):
        if get_object_or_None(RedditPost, _id=s._id):
            print('Post already found.')
            return

        new_rp = RedditPost(_id=s._id, visited=s.visited, url=s.url, title=s.title, json_data=json.dumps(data))
        new_rp.save()

        # for j in data[1]['data']['children'][:-1]:
        #     if j.get('data'):
        #          #new_comment = CommentBuilder(j['data'])
        # #new_comment.children

        return new_rp

    # def children(s):
    #     pass
