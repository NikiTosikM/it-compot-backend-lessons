from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Тут указываем в кортеже те поля которые будут видны при групповом отображении.
    list_display = ('title', 'text')
