from django import forms
from .models import User, Domain


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('id', 'email', 'domain', 'password', 'quota')
        widgets = {
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Password",
                    'autocomplete': "new-password",
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "E-Mail",
                    'autocomplete': "nope",
                }
            ),
            'domain': forms.Select(attrs={
                'class': 'custom-select',

            }),
            'quota': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quota',
                'min': "1",
                'max': "1000",
            })
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['domain'].empty_label = None


class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = {'name'}
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Domain'
                }
            )
        }
