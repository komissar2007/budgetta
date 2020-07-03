from django import template

register = template.Library()


@register.filter(name='get_progress_status')
def get_progress_status(percent):
    if 70 < percent < 100:
        return "progress-bar bg-warning"
    elif percent > 100:
        return "progress-bar bg-danger"
    else:
        return "progress-bar bg-success"
