from django.db import models
from users.models import User
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to='%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='like_articles')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail_view', kwargs={'article_id': self.id})
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content