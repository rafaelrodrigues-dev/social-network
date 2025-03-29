from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

User = get_user_model()

CHOICES = [
    ('M',_('Male')),
    ('F',_('Female')),
    ('S',_('Search me')),
    ('O',_('Other'))
]


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        max_length=20,
        min_length=4,
        label=_('Username'),
    )

    password = forms.CharField(
        widget=forms.PasswordInput()
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

    email = forms.EmailField()

    date_of_birth = forms.DateField(
        widget=forms.SelectDateWidget(years=range(2025,1899,-1)),
        label=_('Date of birth')
    )

    gender = forms.ChoiceField(
        choices=CHOICES,
        label=_('Gender')
    )
    
    def clean_username(self):
        data = self.cleaned_data["username"]
        if User.objects.filter(username=data).exists():
            raise ValidationError(_('This username is already in use'))
        if not data.isalnum():
            raise ValidationError(_('Username must be alphanumeric'))
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise ValidationError(_('This email is already in use'))
        return data


    class Meta:
        model = User
        fields = ('username','first_name','last_name','password','email','date_of_birth','gender')
