from django.shortcuts import render
import smtplib
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings


def home(request):
    return render(request, 'votesite/home.html', {})

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

        return render(request, 'votesite/contact.html', {'firstname': firstname})
    
    else:
        return render(request, 'votesite/contact.html', {})


@login_required
def profile(request):
    username = request.user.first_name
    return render(request, 'votesite/profile.html', {'username': username})