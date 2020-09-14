from django.shortcuts import render, redirect
import smtplib
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import editForm



def home(request):
    if request.user.is_authenticated:
        title = 'Account'
    else:
        title = 'Login'
    return render(request, 'votesite/home.html', {'title' : title})

def handler404(request, exception):
    return render(request, 'votesite/404.html', status=404)

def contact(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        uid = request.POST['uid']
        msg = firstname + ' ' + lastname + '\n' + 'ID: ' + uid + '\n' + email + '\n' + subject + ': ' + message


        connection = smtplib.SMTP('smtp.gmail.com', 587)
        connection.ehlo()
        connection.starttls()
        connection.ehlo()
        username = settings.EMAIL_HOST_USER
        passw = settings.EMAIL_HOST_PASSWORD
        connection.login(username, passw)
        connection.sendmail(
            email,
            [settings.EMAIL_HOST_USER],
            msg
            )

        return render(request, 'votesite/messagesent.html', {'firstname': firstname})
    
    else:
        return render(request, 'votesite/contact.html', {})


@login_required
def profile(request):
    username = request.user.first_name
    return render(request, 'votesite/profile.html', {'username': username})


@login_required
def update(request):
    if request.method == 'POST':
        form = editForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            username = request.user.first_name
            return render(request, 'votesite/profile.html', {'message' : "Form Submitted Successfully!", 'username': username})
    else:
        form = editForm(instance=request.user)
        return render(request, 'votesite/update.html', {'form' : form})