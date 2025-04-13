from django import forms
from django.utils.translation import gettext_lazy as _
from publications.models import Publication

class PublicationForm(forms.ModelForm):
    text = forms.CharField(
        label=_('Text publication'),
        max_length=500,
        widget=forms.Textarea()
    )
    img = forms.ImageField(label=_('Image'),required=False)

    
    class Meta:
        model = Publication
        fields = ("text","img")
