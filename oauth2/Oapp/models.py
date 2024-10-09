from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fortytwo_id = models.CharField(max_length=100, unique=True)
    avatar = models.URLField(max_length=500, null=True, blank=True)
    language = models.CharField(max_length=10, null=True, blank=True)


class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user} is friends with {self.friend}"

