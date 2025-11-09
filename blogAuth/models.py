from django.db import models

# Create your models here.

class captcha(models.Model):
    email = models.EmailField(max_length=254,unique=True)
    code = models.CharField(max_length=6)
    create_time = models.DateTimeField(auto_now_add=True)

