from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    """Строит путь до изображений."""
    if path is None or path == 'avatar_placeholder.jpg':
        return "/media/main/placeholders/avatar_placeholder.jpg"
    return f"/media/{path}"
