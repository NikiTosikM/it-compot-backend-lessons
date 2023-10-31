from django.contrib import admin

from playlist.models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')