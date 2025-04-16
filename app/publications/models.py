from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Publication(models.Model):
    text = models.TextField(_("Text"),max_length=500)
    img = models.ImageField(_("Image"), upload_to='publications/images/%Y/%m/%d/',blank=True,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,related_name='publications',on_delete=models.CASCADE)
    like = models.ManyToManyField(User,related_name='likes',blank=True)

    def __str__(self):
        return f'{self.author.username} publication id:{self.id}'

    
class Comment(models.Model):
    publication = models.ForeignKey(Publication,related_name='comments',on_delete=models.CASCADE)
    text = models.CharField(_("Text"),max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)
    like = models.ManyToManyField(User,related_name='comment_likes',blank=True)

    def __str__(self):
        return f'comment from publication id:{self.publication.id}'
    