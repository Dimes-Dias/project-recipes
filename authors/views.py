from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, RegisterForm

# Create your views here.


def register_view(request):
    # Se register_form_data for enviado por register_create,
    # os dados serão recebidos, tratados e repassados ao formulário.
    # Caso contrário, o formulário irá abrir sem dados (None)
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404('Houve algum problema no envio de dados.')

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    '''
    # se o formulário passar em todos os critérios de validação,
    if form.is_valid():
        # salve os dados no banco de dados
        form.save()
        # manda mensagem para o formulário
        messages.success(request, 'Novo usuário foi criado com sucesso.')
        # limpa os dados de sessão
        del (request.session['register_form_data'])
    else:
        messages.error(
            request, 'Há problemas de validação para este formulário.')
    '''

    if form.is_valid():
        # dessa forma, os dados não serão salvos na base de dados,
        # mas serão gravados numa variável
        user = form.save(commit=False)
        # captura o password digitado e o criptografa antes de salvar
        user.set_password(user.password)
        # salva os dados do formulário na base de dados,
        # porém com a senha criptografada
        user.save()
        # manda mensagem para o formulário
        messages.success(request, 'Novo usuário foi criado com sucesso.')
        # limpa os dados de sessão
        del (request.session['register_form_data'])

        return redirect(reverse('authors:login'))
    else:
        messages.error(
            request, 'Há problemas de validação para este formulário.')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            # se quiser passar mensagem de logado
            messages.success(request, 'Bem vindo, você está logado no sistema.')    # noqa E501
            login(request, authenticated_user)
        else:
            messages.error(request, 'Dados de login inválidos!')
    else:
        messages.error(request, 'Há problemas de validação neste formulário.')

    return redirect(login_url)


# exige que o usuário esteja logado para ter acesso a view
@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    # segurança: não aceita logout por GET
    if not request.POST:
        return redirect(reverse('authors:login'))

    # segurança: não aceita logout de outro usuário no usuário corrente
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    # se estiver tudo certo, faz logout antes de redirecionar
    logout(request)
    return redirect(reverse('authors:login'))
