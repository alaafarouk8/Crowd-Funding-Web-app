from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Users
from django.contrib.auth import authenticate




class RegistraionForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = Users
        fields = ('email','username','first_name','last_name','phone','photo','password1','password2')

#================================================================================================
class LoginForm(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput)
    class Meta:
        model = Users
        fields = ('email','password', 'is_active')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError('invalid login data...')

#===================================================================================================

class DateInput(forms.DateInput):
    input_type = 'date'


class UpdateUserForm(forms.ModelForm):
    date_birth = forms.DateField(required=False,widget=DateInput())
    photo = forms.ImageField(required=False,widget=forms.FileInput)
    facebook_link = forms.URLField(required=False)
    country = forms.CharField(required=False)
    class Meta:
        model = Users
        fields = ('first_name','last_name','phone','photo','date_birth','facebook_link','country')

    def clean_country(self):
        if self.is_valid():
            country = self.cleaned_data['country']
            if country:
                return country
            else :
                return None


    def clean_facebook_link(self):
        if self.is_valid():
            facebook_link = self.cleaned_data['facebook_link']
            if facebook_link:
                return facebook_link
            else :
                return None


    def clean_date_birth(self):
        if self.is_valid():
            date_birth = self.cleaned_data['date_birth']
            if date_birth:
                return date_birth
            else :
                return None
