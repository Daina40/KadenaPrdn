from django import template

register = template.Library()

@register.filter
def get_comment(comments_dict, process):
    return comments_dict.get(process, "")

