from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')

@register.filter
def class_name(value):
    return value.__class__.__name__ if value is not None else 'None'

@register.filter
def get_grade(checklist, subject_code):
    """
    Get the grade for a specific subject from the checklist
    """
    if not checklist:
        return ""
    
    field_name = subject_code.replace(' ', '_').lower()
    return getattr(checklist, field_name, "")
