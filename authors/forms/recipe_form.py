from collections import defaultdict

from attr import fields
from django import forms
from django.forms import ValidationError
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_erros = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
        }

    # validação geral
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cd = self.cleaned_data
        title = cd.get('title')
        description = cd.get('description')

        # verifica um erro de quantidade de caracteres em title
        # if len(title) < 5:
        #     self._my_erros['title'].append(
        #         'O título deve ter pelo menos 5 caracteres.'
        #     )

        # ----------------------------------------------------
        # verifica outros erros em title ou outros campos
        # ----------------------------------------------------
        if title == description:
            self._my_erros['title'].append(
                'Não pode ser igual a Descrição.'
            )
            self._my_erros['description'].append(
                'Não pode ser igual a Título.'
            )

        # levanta os erros encontrados
        if self._my_erros:
            raise ValidationError(self._my_erros)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_erros['title'].append(
                'O título deve ter pelo menos 5 caracteres.'
            )

        return title

    def valid_field_number_positive(self, field_name):
        field_value = self.cleaned_data.get(field_name)
        if not is_positive_number(field_value) is True:
            self._my_erros[field_name].append('Deve ser um número positivo')

        return field_value

    def clean_preparation_time(self):
        return self.valid_field_number_positive('preparation_time')

    def clean_servings(self):
        return self.valid_field_number_positive('servings')
