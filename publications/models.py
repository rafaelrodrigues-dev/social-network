from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class Publication(models.Model):
    text = models.TextField(_("Text"))
    img = models.ImageField(_("Image"), upload_to='publications/images/%Y/m%/%d',blank=True,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username} {self.id}'
    