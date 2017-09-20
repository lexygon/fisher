from django import template

register = template.Library()


@register.simple_tag
def get_query(request, rm_fields='', **kwargs):
    if rm_fields:
        rm_fields = rm_fields.split(',')

    updated = request.GET.copy()

    for k, v in kwargs.items():
        if k not in rm_fields:
            updated[k] = v

    for k, v in list(updated.items()):
        if k in rm_fields:
            del updated[k]

    return updated.urlencode()
