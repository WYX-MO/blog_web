from django import forms
from blogMain.models import BlogCategory

class BlogPostForm(forms.Form):
    title = forms.CharField(max_length=100,min_length=2,label='标题')
    content = forms.CharField(min_length=2,label='内容')
    category = forms.IntegerField(label='分类')
