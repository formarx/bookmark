from django.shortcuts import render
from django.contrib import auth
from .forms import RegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            new_user.set_password(password)
            new_user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return render(request, 'registration/register_done.html', {'new_user':new_user})
    else:
        user_form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form':user_form})
