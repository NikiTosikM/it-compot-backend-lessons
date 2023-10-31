

```python
class Post(models.Model):
    title = models.CharField(max_length=70)
    image = models.ImageField(upload_to='images/')
    text = models.TextField()
    likes = models.IntegerField(blank=True)
    rating = models.FloatField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Название объекта модели для django ui. (В админке например используется)
        verbose_name = 'Пост' 
        # Во множественном числе.
        verbose_name_plural = 'Посты'
    
    def __str__(self):
        # Интерпритация класса в str
        return self.title  
```