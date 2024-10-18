from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        default='default.png'
    )
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=10, null=True, blank=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    win_rate = models.FloatField(default=0)
    win_streak = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Friend(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_BLOCKED = 'blocked'

    STATUS = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_BLOCKED, 'Blocked'),
    ]

    user = models.ForeignKey(User, related_name='friend_user', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_friend', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default=STATUS_PENDING)
    two_fa_code = models.CharField(max_length=6, blank=True, null=True)
    two_fa_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"




class Game(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'

    GAME_STATUS = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
    ]
    player1 = models.ForeignKey(User, related_name='player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='player2', on_delete=models.CASCADE)
    winner = models.ForeignKey(User, related_name='winner', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    game_length = models.IntegerField() #seconds
    player1_score = models.IntegerField()
    player2_score = models.IntegerField()
    status = models.CharField(max_length=100,choices=GAME_STATUS, default=STATUS_PENDING)

    def __str__(self):
        return f"{self.player1.username} vs {self.player2.username} on {self.date}"

class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user} is friends with {self.friend}"
