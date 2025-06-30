from django import template
from django.utils.translation import get_language
from django.conf import settings
import logging

register = template.Library()
logger = logging.getLogger(__name__)

@register.simple_tag
def available_languages():
    # Log the available languages instead of printing
    # logger.debug("Available languages: %s", settings.LANGUAGES)
    return settings.LANGUAGES

@register.simple_tag
def current_language():
    # Log the current language
    # logger.debug("Current language: %s", get_language())
    return get_language()
