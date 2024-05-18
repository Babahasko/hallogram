from django.db import models
from django.conf import settings
import uuid

from django.urls import reverse, reverse_lazy


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(default=None, blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

    def get_absolute_url(self):
        return reverse_lazy(viewname='profile', kwargs={'profile_uuid': self.uuid})
# Create your models here.
