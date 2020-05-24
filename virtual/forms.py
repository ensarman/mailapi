from django import forms
from .models import User

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'domain', 'password', 'quota')
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': "Password",
                'autocomplete': "new-password",
            }),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "E-Mail"}),
            'domain': forms.Select(attrs={'class': 'custom-select'}),
            'quota': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quota'})
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['domain'].empty_label = None
