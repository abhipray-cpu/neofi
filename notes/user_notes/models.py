from django.db import models
from users.models import User
# Create your models here.
class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, verbose_name='note_owner')
    content = models.TextField(null=False, default='Create your note', verbose_name='note_content')
    object = models.Manager()
    share = models.TextField(null=False, default='[]', verbose_name='shared_users')

class Change(models.Model):
    user = models.IntegerField(null=True, verbose_name='changed_by')
    note = models.IntegerField(null=False, verbose_name='note_id')
    prev = models.TextField(null=False, verbose_name='old_content')
    new = models.TextField(null=False, verbose_name='new_content')
    date = models.DateField(auto_now_add=True, null=True)
    object = models.Manager()

