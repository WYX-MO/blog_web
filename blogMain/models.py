from django.db import models

# Create your models here.

class BlogCategory(models.Model):
    name = models.CharField(max_length=100,unique=True,null=False)    
    class Meta:
        db_table = 'blog_category'
    def __str__(self):
        return self.name
    

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    publicTime = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_DEFAULT,default=1)
    auther = models.ForeignKey('auth.User', on_delete=models.SET_DEFAULT,default=1)
    class Meta:
        db_table = 'blog_post'
        ordering = ['-publicTime']
    def __str__(self):
        return self.title
    
class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE,related_name='comments')
    auther = models.ForeignKey('auth.User', on_delete=models.SET_DEFAULT,default=1)
    content = models.TextField(null=False)
    publicTime = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'blog_comment'
        ordering = ['-publicTime']
    def __str__(self):
        return self.content[:20]