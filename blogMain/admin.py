from django.contrib import admin
from .models import BlogCategory,BlogPost,BlogComment
# Register your models here.
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    sortable_by = ('id')

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = '博客分类'

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id','title','content','publicTime','category','auther')
    sortable_by = ('publicTime')
    class Meta:
        verbose_name = '博客文章'
        verbose_name_plural = '博客文章'

class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('id','post','auther','content','publicTime')
    sortable_by = ('post')
    class Meta:
        verbose_name = '博客评论'
        verbose_name_plural = '博客评论'


admin.site.register(BlogCategory,BlogCategoryAdmin)
admin.site.register(BlogPost,BlogPostAdmin)
admin.site.register(BlogComment,BlogCommentAdmin)
