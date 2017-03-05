from django.db import models


class RedditPost(models.Model):

    url = models.CharField(max_length=1000)
    title = models.TextField()

    json_data = models.TextField(null=True)

    visited = models.BooleanField(default=False)
    loaded = models.BooleanField(default=False)

    _id = models.CharField(max_length=100, null=True)

    #children = models.ForeignKey("Comment", null=True, related_name=)

    def __str__(s):
        return 'Post: "%s"' % (s.title,)  # s.url)

    # def children(s):

    @property
    def score(s):
        return None


class Comment(models.Model):

    _id = models.CharField(max_length=100, null=True)
    body = models.TextField(null=True)
    score = models.IntegerField(null=True)
    name = models.CharField(max_length=100, null=True)
    reddit_parent_id = models.CharField(max_length=100, null=True)

    reddit_post = models.ForeignKey(RedditPost, related_name="children")
    children = models.ManyToManyField("Comment")
    parent = models.ForeignKey("Comment", related_name="_children", null=True)

    visited = models.BooleanField(default=False)

    def __str__(s):
        return '(%s) %s' % (s.post_title_stub, s.body)

    @property
    def post_title_stub(s):
        return s.reddit_post.title[:10]+'...' if s.reddit_post else '?'

    @property
    def num_children(s):
        return s.children.objects.count()

    @property
    def short_body(s):
        return s.body[:100]+'...'


class Increase(models.Model):

    reddit_post = models.ForeignKey(RedditPost, null=True)

    parent_comment = models.ForeignKey(Comment, related_name='parent_increases')
    child_comment = models.ForeignKey(Comment, related_name='child_increases')

    percent = models.IntegerField(null=True)

    def __str__(s):
        return '(%s) (+%s%%) (%s->%s) %s >> %s' % (s.parent_comment.post_title_stub,
                                                   s.percent, s.parent_comment.score, s.child_comment.score,
                                                   s.parent_comment.body[:10], s.child_comment.body[:10])
