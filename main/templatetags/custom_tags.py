from django import template

register = template.Library()


@register.filter()
def media_filter(path: str) -> str:
    """Строит путь до изображений."""
    if path == '' or path == 'avatar_placeholder.jpg':
        return "/media/main/placeholders/avatar_placeholder.jpg"
    return f"/media/{path}"


@register.filter()
def years_declination_filter(years: int) -> str:
    """Пишет правильное склонение, например 1 год, 2 года, 5 лет."""
    word = ''
    if years == 1:
        word = 'год'
    if 1 < years < 5:
        word = 'года'
    if 4 < years < 21 or years == 0:
        word = 'лет'
    if years > 20:
        years_second_number = int(str(years)[1])
        if years_second_number == 1:
            word = 'год'
        if 1 < years_second_number < 5:
            word = 'года'
        if 4 < years_second_number < 10 or years_second_number == 0:
            word = 'лет'
    return f'{years} {word}'
