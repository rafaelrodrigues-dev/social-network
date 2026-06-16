from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Author(AbstractUser):
    date_of_birth = models.DateField(_("Date of birth"),null=True,blank=True)
    gender = models.CharField(_("Gender"), max_length=50)

    @property
    def has_unread_notifications(self):
        return self.notifications.filter(is_read=False).exists()

