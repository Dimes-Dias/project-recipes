from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu nome de usuário')
        add_placeholder(self.fields['email'], 'Seu e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: Dimes')
        add_placeholder(self.fields['last_name'], 'Ex.: Dias')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['password2'], 'Repita sua senha')

    username = forms.CharField(
        label='Nome de usuário',
        help_text=(
            'O nome de usuário deve ter letras, números ou um desses símbolos @ .+-_. '  # noqa E501
            'O comprimento deve estar entre 4 e 150 caracteres.'
        ),
        error_messages={
            'required': 'Este campo não deve estar vazio',
            'min_length': 'O nome de usuário deve ter no mínimo 4 caracteres',
            'max_length': 'O nome de usuário deve ter no máximo 150 caracteres',    # noqa E501
        },
        min_length=4, max_length=150,
    )
    first_name = forms.CharField(
        error_messages={'required': 'Escreva seu primeiro nome'},
        label='Primeiro nome'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Escreva seu último nome'},
        label='Último nome'
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail é obrigatório'},
        label='E-mail',
        help_text='O e-mail deve ser válido.',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'A senha não deve estar vazia.'
        },
        help_text=(
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O comprimento deve ser de '
            'pelo menos 8 caracteres.'
        ),
        validators=[strong_password],
        label='Senha'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmação da senha',
        error_messages={
            'required': 'Por favor, digite a senha novamente.'
        },
    )

    # criamos a class Meta para detalhar o que
    # será usado do model User no formulário

    class Meta:
        # vincula o model User
        model = User
        # vincula todos os campos...
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    # clean_* é o método para validar o campo específico
    # exemplos: clean_email, clean_first_name, clean_password, etc.
    def clean_email(self):
        # cleaned_data é usado para pegar o valor do campo
        email = self.cleaned_data.get('email', '')
        # filtra o campo email com base na variável email,
        # e verifica se já existe.
        # o primeiro email é o campo, o segundo é a variável
        exists = User.objects.filter(email=email).exists()

        if exists:
            # ValidationError vai retornar mensagem de erro, se houver
            raise ValidationError(
                'O e-mail do usuário já está em uso',
                code='invalid',
            )

        return email

    # após a validação individual de cada campo,
    # o django chama o método a seguir,
    # para uma validação do form como um todo.
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            # levanta uma mensagem de erro e atribui a uma variável
            password_confirmation_error = ValidationError(
                'Senha e Confirmação devem ser iguais',
                code='invalid'
            )
            # lança a variável com a mensagem de erro a ambos os campos de senha    # noqa E501
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
