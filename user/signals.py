from django.contrib.auth.models import User
from relationship.models import Relationship

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)




def follow(self, user):
    if self != user:  # Prevent users from following themselves
        Relationship.objects.get_or_create(follower=self, following=user)

def unfollow(self, user):
    Relationship.objects.filter(follower=self, following=user).delete()

def is_following(self, user):
    return Relationship.objects.filter(follower=self, following=user).exists()

def get_followers(self):
    """Get all followers of this user."""
    return Relationship.objects.filter(following=self)

def get_following(self):
    """Get all users this user is following."""
    return Relationship.objects.filter(follower=self)

def followers_count(self):
    return self.get_followers().count()

def following_count(self):
    return self.get_following().count()

# Add methods dynamically to the User model
User.add_to_class("follow", follow)
User.add_to_class("unfollow", unfollow)
User.add_to_class("is_following", is_following)
User.add_to_class("followers_count", followers_count)
User.add_to_class("following_count", following_count)
User.add_to_class("get_followers", get_followers)
User.add_to_class("get_following", get_following)