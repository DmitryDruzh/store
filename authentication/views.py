from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import LoginForm, RegisterForm

# Create your views here.

def login_user(request):
    context = {'login_form': LoginForm}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
        else:
            context = {
                'login_form': login_form,
            }
    return render(request, 'auth/login.html', context)


class RegisterView(TemplateView):
    template_name = 'auth/register.html'

    def get(self, request):
        register_form = RegisterForm()
        context = {'register_form': register_form}
        return render(request, 'auth/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('index')

        context = {'register_form': register_form}
        return render(request, 'auth/register.html', context)




def logout_user(request):
    logout(request)
    return redirect('index')
