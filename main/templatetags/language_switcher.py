from django import template
from django.utils.translation import get_language
from django.conf import settings

register = template.Library()

@register.simple_tag
def available_languages():
    print("Available languages:", settings.LANGUAGES)
    return settings.LANGUAGES

@register.simple_tag
def current_language():
    print("Current language:", get_language())
    return get_language()
