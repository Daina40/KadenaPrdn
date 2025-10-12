from django import template

register = template.Library()

@register.filter
def get_comment_for_desc(comments_dict, desc_id):
    return comments_dict.get(desc_id, {})

@register.filter
def get_comment(process_dict, process_name):
    return process_dict.get(process_name.strip(), "")
