from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'register/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'register/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        # create a new user
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            # login user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            login(request, authenticate(username=username, password=password))

            return redirect('home')
        else:
            return render(request, 'register/signup.html', {'form': form})
    else:
        # show the form
        form = UserCreationForm()
        return render(request, 'register/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
