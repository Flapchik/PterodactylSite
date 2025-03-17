from django import template
import datetime

register = template.Library()

@register.filter
def format_size(value):
    """Форматирует размер файла в более читаемый вид (КБ, МБ, ГБ)"""
    try:
        value = int(value)
        if value < 1024:
            return f"{value} Б"
        elif value < 1024**2:
            return f"{value / 1024:.1f} КБ"
        elif value < 1024**3:
            return f"{value / 1024**2:.1f} МБ"
        else:
            return f"{value / 1024**3:.1f} ГБ"
    except (ValueError, TypeError):
        return value

@register.filter
def format_date(value):
    """Форматирует дату в читаемый вид"""
    try:
        dt = datetime.datetime.fromisoformat(value)
        return dt.strftime("%d.%m.%Y %H:%M")
    except ValueError:
        return value
