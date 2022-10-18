from django import forms
from utils.django_forms import add_placeholder


class LoginForm(forms.Form):
    def __ini__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite o seu usuário')
        add_placeholder(self.fields['password'], 'Digite a sua senha')

    username = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha',
                               widget=forms.PasswordInput()
                               )
