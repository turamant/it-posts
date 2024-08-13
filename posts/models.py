from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.title
        

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_posts')
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_posts')
    content = models.TextField()
    created_at = models.DateTimeField()
    
    @property
    def excerpt(self):
        return Truncator(self.content).chars(148)
    
    
    def __str__(self):
        return self.title
    
