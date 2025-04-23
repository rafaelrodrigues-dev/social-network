from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from profiles.models import Profile

User = get_user_model()

CHOICES = [
    ('M',_('Male')),
    ('F',_('Female')),
    ('S',_('Search me')),
    ('O',_('Other'))
]


class EditAuthorForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user',None)
        super().__init__(*args, **kwargs)
    
        if user and hasattr(user,'profile'):
            self.fields['picture'].initial = user.profile.picture
            self.fields['bio'].initial = user.profile.bio

    username = forms.CharField(
        max_length=20,
        min_length=4,
        label=_('Username'),
    )

    first_name = forms.CharField(
        max_length=30,
        label=_('First name')
    )

    last_name = forms.CharField(
        max_length=30,
        required=False,
        label=_('Last name')
    )

    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=range(2025,1899,-1)),
        label=_('Date of birth')
    )

    gender = forms.ChoiceField(
        choices=CHOICES,
        label=_('Gender')
    )
    # Profile Model fields
    picture = forms.ImageField(
        label=_('Picture'),
        required=False,
        widget=forms.ClearableFileInput(attrs={'class':'custom-file-input'})
    )

    bio = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label=_('Bio')
    )
    
    def save(self, commit = True):
        user = super().save(commit)
        picture = self.cleaned_data.get('picture')
        bio = self.cleaned_data.get('bio')

        if hasattr(user,'profile'):
            profile = user.profile
        else:
            profile = Profile(user=user)

        profile.picture = picture
        profile.bio = bio

        if commit:
            profile.save()
        
        return user


    class Meta:
        model = User
        fields = ('username','first_name','last_name','date_of_birth','gender')
