
from django.urls import include, path, re_path

from django.conf.urls import url
from users.views import register, user_login, activate, index
from django.conf import settings
from django.conf.urls.static import static
from users import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView
from .views import userprofile
from rest_framework import routers
from .views import usersListView
app_name = 'users'
router = routers.DefaultRouter()
router.register(r'usersListView', usersListView)

urlpatterns = [

    path('register', views.register , name='register'),
    path('activate/<uidb64>/<time>',views.activate, name='activate'),
    path('login/', views.user_login , name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('userprofile', views.userprofile  , name="userprofile"),
    path('deleteprofile/<int:id>/' , views.deleteprofile , name="deleteprofile"),
    path('editprofile' , views.editprofile , name="editprofile"),
    path('users', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('logout/',views.logout_view,name='logout'),
    #  path('profile',views.user_profile,name="profile"),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_reset/password_change_done.html'),
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_reset/password_change.html'),
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset/password_change.html'), name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset/password_reset_form.html'), name='password_reset'),


    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset/password_reset_complete.html'),
     name='password_reset_complete'),

    url('^', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
