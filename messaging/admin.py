from django.contrib import admin
from .models import Message, Reply, Reaction, Profile, Task

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'text_preview', 'timestamp', 'total_reactions')
    search_fields = ('author__username', 'text')
    list_filter = ('timestamp', 'author')
    readonly_fields = ('timestamp',)
    
    def text_preview(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_preview.short_description = 'Mesaj'
    
    def total_reactions(self, obj):
        return obj.like_count + obj.laugh_count + obj.sad_count + obj.fire_count + obj.thumbs_up_count + obj.angry_count
    total_reactions.short_description = 'Toplam Tepkiler'

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('author', 'message', 'timestamp')
    search_fields = ('author__username', 'text')
    list_filter = ('timestamp',)
    readonly_fields = ('timestamp',)

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'reaction_type')
    search_fields = ('user__username', 'reaction_type')
    list_filter = ('reaction_type',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'created_at')
    search_fields = ('user__username', 'location')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at', 'completed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Görev Bilgileri', {
            'fields': ('title', 'description', 'status')
        }),
        ('Tarihler', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
