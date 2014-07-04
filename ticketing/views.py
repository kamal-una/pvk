from django.shortcuts import render
from django.shortcuts import redirect
from django.http import StreamingHttpResponse
from forms import UserForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
import logging


# Create your views here.
def home(request):
    context = {}

    html = render(request, 'home.html', context)
    return StreamingHttpResponse(html)


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print "form not valid!"
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


@login_required
def my_account(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            new_user = form.save()
    form = UserForm(instance=request.user)
    return render(request, "my_account.html", {'form': form})


@login_required
def user_logout(request):
    # empty the cart
    logout(request)
    return redirect('login')

