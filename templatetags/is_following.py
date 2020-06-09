from django import template

from ..models import *

register = template.Library()


@register.simple_tag(name="is_following", takes_context=True)
def is_following(context, user):
    request = context['request']
    return Following.objects.filter(user=user, follower=request.user).exists()
