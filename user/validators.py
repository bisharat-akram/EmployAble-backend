from django.core.validators import RegexValidator

phone_validator = RegexValidator(regex = '^\+?1?\d{9,15}$',message = 'Mobile is not in correct format',code = 400)

