from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    laugh_count = models.IntegerField(default=0)
    sad_count = models.IntegerField(default=0)
    fire_count = models.IntegerField(default=0)
    thumbs_up_count = models.IntegerField(default=0)
    angry_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author.username}: {self.text[:50]}"

class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10)

    class Meta:
        unique_together = ('user', 'message')

    def __str__(self):
        return f"{self.user.username} reacted {self.reaction_type} to {self.message}"

class Reply(models.Model):
    message = models.ForeignKey(Message, related_name='replies', on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    emoji = models.CharField(max_length=10, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.text:
            return f"Reply by {self.author.username}: {self.text[:50]}"
        else:
            return f"Reply by {self.author.username}: {self.emoji}"
