from django.db import models
from django.utils. translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    picture = models.ImageField(_("Picture"), upload_to='profiles/picture',null=True,blank=True)
    bio = models.CharField(_("Bio"), max_length=50,blank=True)
    follow = models.ManyToManyField("self",symmetrical=False,related_name='followers',blank=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    
    def get_absolute_url(self):
        return reverse("profiles:profile", kwargs={"username": self.user.username})
    
    def __str__(self):
        return f'{self.user} profile'
