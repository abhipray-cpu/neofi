from django.db import models
from django.core.validators import EmailValidator,MinLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
import re
# Create your models here.
def contact_validator(value):
    pattern = r'^\d{10}$'
    if not re.match(pattern, value):
        raise ValidationError('Please enter a valid contact number.')

class User(AbstractUser):
    name = models.CharField(max_length=100, null=False, verbose_name='user_name')
    email = models.EmailField(max_length=254, unique=True, null=False,
                              validators=[EmailValidator(message='Enter a valid email address.')],
                              verbose_name='user_email')
    contact = models.CharField(max_length=10, unique=True, null=False, verbose_name='user_contact',
                               validators=[contact_validator])
    password = models.CharField(validators=[MinLengthValidator(8)], verbose_name='user_password', max_length=100)
    objects = models.Manager()
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # hashing the password before saving it
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)