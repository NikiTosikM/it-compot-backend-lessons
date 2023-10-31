from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField()
    likes = models.IntegerField(blank=True)
    rating = models.FloatField(blank=True)
    image = models.ImageField(upload_to='images/')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title