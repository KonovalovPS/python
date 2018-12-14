from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class User(models.Model):
    # login = models.CharField('login', max_length=40)
    # password = models.CharField('password', max_length=100)
    # nickname = models.CharField('nickname', max_length=100)
    # #avatar
    # def __str__(self):
        # return f'{self.nickname}'

class Blogg(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    blog_name = models.CharField('blog name', max_length=100, default = '')
    
    def __str__(self):
        return f'{self.blog_name}'    
    
class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    blog_id = models.ForeignKey(Blogg, on_delete=models.PROTECT)
    headline = models.CharField('headline', max_length=60)
    text = models.TextField('text', max_length=600)
    pub_date = models.DateTimeField('pub date', auto_now_add=True)
    views = models.IntegerField('views', default = 0)
    hidden = models.BooleanField('hidden', default=False)
    
    
    def __str__(self):
        return f'{self.headline}'
    
class Comment(models.Model):
    comment_text = models.TextField('comment', max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    post_id = models.ForeignKey(Post, on_delete=models.PROTECT)
    pub_date = models.DateTimeField('pub date', auto_now_add=True)
    
    def __str__(self):
        return f'{self.comment_text}'