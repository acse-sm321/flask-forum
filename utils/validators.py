import re

from wtforms import ValidationError


def phone_required(form, field):
    """Verify the input mobile number"""
    username = field.data
    pattern = r'1[0-9]{10}$'
    if not re.search(pattern, username):
        raise ValidationError('Please enter your phone number')
    return field
