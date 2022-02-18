from users.forms import RegistraionForm, LoginForm, UpdateUserForm
from django.shortcuts import render, redirect, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from users.models import Users
import datetime
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .serializers import usersSerializer
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from fundproject.models import Project


@api_view(['GET', 'DELETE', 'PUT'])
def userView(request, id):
    try:
        user = Users.objects.get(id=id)
    except Users.DoesNotExist:
        return Response("HTTP_404_NOT_FOUND")
    if request.method == 'DELETE':
        user.delete()
        return Response({'msg', f'user deleted'})
    elif request.method == 'GET':
        res = usersSerializer(user, context={'request': request})
        return (res.data)
    elif request.method == 'PUT':
        req_update = usersSerializer(user, data=request.data, context={'request': request})
        if req_update.is_valid():
            req_update.save()
            return Response(req_update.data)
        else:
            return Response(req_update.errors)
    else:
        return Response({'msg': 'None'})


class usersListView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = usersSerializer


# Create your views here.
def register(request):
    context = {}
    if request.method == 'POST':
        form = RegistraionForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            print(user)
            send_email(
                user,
                get_current_site(request),
                form.cleaned_data.get("email"),
                "users/account_activation.html",
                "Activate your account.",
            )
            return render(request, "users/sending_email.html", {"active_code": -1})
        else:
            context["form"] = form
    else:
        form = RegistraionForm()
    return render(request, 'users/new-register.html', {'form': form})


def send_email(user, current_site, email, email_body, email_subject):
    mail_subject = email_subject
    message = render_to_string(
        email_body,
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "time": urlsafe_base64_encode(force_bytes(datetime.datetime.now())),
        },
    )
    to_email = email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def activate(request, uidb64, time):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print("user id : ", uid)
        time_sent = force_text(urlsafe_base64_decode(time))
        user = Users.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError):
        user = None
    if user is not None:
        if user.is_active == False:
            email_sent_at = time_sent
            date_diffrince = (
                                     datetime.datetime.now()
                                     - datetime.datetime.strptime(email_sent_at,
                                                                  "%Y-%m-%d %H:%M:%S.%f")
                             ).seconds / 60

            if date_diffrince < (24 * 60):
                user.is_active = True
                user.save()
                return render(
                    request, "users/sending_email.html", {"active_code": 1}
                )
            else:
                current_site = get_current_site(request)
                email = user.email
                send_email(
                    user,
                    current_site,
                    email,
                    "users/account_activation.html",
                    "Activate your account.",
                )
                return render(
                    request, "users/sending_email.html", {"active_code": 0}
                )
        else:
            return render(request, "users/sending_email.html", {"active_code": 2})
    else:
        return render(request, "users/sending_email.html", {"active_code": 3})


def user_login(request):
    # if request.user.is_authenticated:
    #     return redirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=Users.objects.get(email=email), password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print(user)
                    request.session['usernew']=user.first_name
                    return render(request, "users/index.html")
            # else:
            #     messages.info(request,'invalid login data...')
    else:
        form = LoginForm()

    return render(request, 'users/new-login.html', {'form': form})


@login_required(login_url='/login')
def index(request):
    context = {
        "user": request.username
    }
    return render(request, "users/index.html", context)


# # #####
def logout_view(request):
    request.session.clear()
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def userprofile(request):
    if not request.user.is_authenticated:
        return redirect(reverse("users:login"))
    return render(request, "users/userprofile.html")


@login_required(login_url='/login')
def deleteprofile(request, id):
    queryset = Users.objects.get(id=id)
    if request.method == 'POST':
        queryset.delete()
        logout(request)
    return render(request, "users/deleteprofile.html")


@login_required(login_url='/login')
def editprofile(request):
    form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            print("photo from form is :", form.cleaned_data["photo"])
            request.user.photo = form.cleaned_data["photo"]
            form.save()
            return redirect(reverse("users:userprofile"))
        else:
            form = UpdateUserForm(
                initial={
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                    "phone": request.user.phone,
                    "date_birth": request.user.date_birth,
                    "facebook_link": request.user.facebook_link,
                    "country": request.user.country,

                }
            )
        # context={"form": form}
    return render(request, "users/editprofile.html", {"form": form})


@login_required(login_url='/login')
def userproject(request, id):
    user = Users.objects.get(id=id)
    # projects = Project.objects.filter(
    #     user=user)  # first user => forign key , second user is user which get by the previous line
    # context = {
    #     "user": user,
    #     "projects": projects
    # }

    return render(request, "users/userproject.html")


@login_required(login_url='/login')
def userdonation(request , id):
     user = Users.objects.get(id=id)
     return render(request, "users/userdonation.html")
