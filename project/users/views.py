# from django.shortcuts import render
# from django.http import HttpResponse
#
# # Create your views here.
# def test(request):
#     return HttpResponse('worked ')
#
# def register(request):
#      return HttpResponse('register page')
#

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
            user = authenticate(email=Users.objects.get(email=email) ,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return render(request, "users/index.html")
            # else:
            #     messages.info(request,'invalid login data...')
    else:
        form = LoginForm()
    return render(request, 'users/new-login.html', {'form' : form})

@login_required(login_url='/login')
def index(request):
    return render(request, "users/index.html")
# #
# def logout_view(request):
#     logout(request)
#     return redirect('/login')

# @login_required(login_url='/login')
# def edit_user_profile(request):
#     form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
#     if request.POST:
#         if form.is_valid():
#             print("photo from form is :", form.cleaned_data["photo"])
#             request.user.photo = form.cleaned_data["photo"]
#             form.save()
#             return redirect(reverse("users:profile"))
#     else:
#         form = UpdateUserForm(
#             initial={
#                 "first_name": request.user.first_name,
#                 "last_name": request.user.last_name,
#                 "phone": request.user.phone,
#                 "date_birth": request.user.date_birth,
#                 "facebook_link": request.user.facebook_link,
#                 "country": request.user.country,
#             }
#         )
#     context = {"form": form}
#     return render(request, "users/edit_user_profile.html", context=context)
#
# @login_required(login_url='/login')
# def user_profile(request):
#     if not request.user.is_authenticated:
#         return redirect(reverse("users:login"))
#     return render(request, "users/new-user_profile.html")
#
# def send_delete_email(request):
#     user = request.user
#     current_site = get_current_site(request)
#     email = user.email
#     email_subject = "Delete your account"
#     email_body = "users/sending_email_on_delete.html"
#     send_email(user, current_site, email, email_body, email_subject)
#     return render(request, "users/delete_account.html", {"delete_code": -1})
#
# @login_required(login_url='/login')
# def delete_account(request, uidb64, time):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         time_sent = force_text(urlsafe_base64_decode(time))
#         user = Users.objects.get(pk=uid)
#
#     except (TypeError, ValueError, OverflowError):
#         user = None
#     if user is not None:
#         email_sent_at = time_sent
#         date_diffrince = (
#             datetime.datetime.now()
#             - datetime.datetime.strptime(email_sent_at, "%Y-%m-%d %H:%M:%S.%f")
#         ).seconds / 60
#
#         if date_diffrince < (24 * 60):
#             user.delete()
#             logout(request)
#             return render(
#                 request, "users/delete_account.html", {"delete_code": 1}
#             )
#         else:
#             current_site = get_current_site(request)
#             email = user.email
#             send_email(
#                 user,
#                 current_site,
#                 email,
#                 "users/sending_email_on_delete.html",
#                 "Delete your account.",
#             )
#             return render(
#                 request, "users/delete_account.html", {"delete_code": 0}
#             )
#     else:
#         return render(request, "users/delete_account.html", {"delete_code": 2})
