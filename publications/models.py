from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Publication(models.Model):
    text = models.TextField(_("Text"))
    img = models.ImageField(_("Image"), upload_to='publications/images/%Y/%m/%d/',blank=True,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='likes',blank=True)

    def __str__(self):
        return f'{self.author.username} publication id:{self.id}'
    