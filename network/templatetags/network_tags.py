from django import template
from ..models import Follow

register = template.Library()

@register.filter
def is_following(user, this_user):
    if not user or not user.is_authenticated:
        return False
    is_following = Follow.objects.filter(follower=user, following=this_user).exists()
    return is_following