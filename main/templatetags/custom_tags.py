from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    """Строит путь до изображений."""
    if path:
        return f"/media/{path}"
    return "/media/user/avatar/avatar_placeholder.webp"
