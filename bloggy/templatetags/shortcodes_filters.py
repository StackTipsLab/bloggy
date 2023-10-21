from django import template

from bloggy.shortcodes import parser

register = template.Library()


def shortcodes_replace(value):
    return parser.parse(value)


register.filter('shortcodes', shortcodes_replace)
