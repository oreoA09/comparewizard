from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, UpdateUserForm, UpdateProfileForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            # return redirect("dashboard:workspace.html")
            return redirect('project')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("Incorrect Password, try again"))
            return redirect('login')
    else:
        return render(request, 'registration/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You've been Logged out"))
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Sign up successful!"))
            return redirect('login')
    else:
        form = RegisterUserForm()
    return render(request, 'registration/register.html', {
        'form':form,
    })

# @login_required
# def profile_user(request):
#   return render(request, 'registration/profile.html')


@login_required
def profile_user(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'registration/profile.html', {'user_form': user_form, 'profile_form': profile_form})

# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('change_password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
    # return render(request, 'accounts/change_password.html', {
    #     'form': form
    # })
    # return render(request, 'registration/password_change_form.html')


def password_done(request):
    return render(request, 'registration/password_change_done.html')
