from django.contrib import admin
from .models import Relationship

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')