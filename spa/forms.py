from django import forms

from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm, ReadOnlyPasswordHashField
from pkg_resources import _

from spa.models import CustomUser, UserSubscription
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser #, Company
# from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError

class CustomUserRegistrationForm(forms.ModelForm):
    is_staff = forms.BooleanField(label='staff status')
    # firstname = forms.CharField(label = 'First Name*', max_length = 120)
    # lastname = forms.CharField(label = 'Last Name*', max_length = 120)
    email = forms.EmailField(label = 'Email*')
    # phone = PhoneNumberField()
    # company = forms.ModelChoiceField(queryset = Company.objects.all(), label = 'Company*', required = True)
    password = forms.CharField(label = 'Password*', min_length = 5, max_length = 50, widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Confirm Password*', min_length = 5, max_length = 50, widget = forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_staff')#'firstname', 'lastname', 'company','phone',

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user_list = CustomUser.objects.filter(email=email)
        if user_list.count():
            raise ValidationError('There is already an account associated with that email.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if (password1 and password2) and (password1 != password2):
            raise ValidationError('Passwords do not match.')
        return password2

    def save(self, commit=True):
        context = {
            # 'firstname':self.cleaned_data['firstname'],
            # 'lastname':self.cleaned_data['lastname'],
            'email':self.cleaned_data['email'],
            # 'phone':self.cleaned_data['phone'],
            'password':self.cleaned_data['password'],
            'admin':'',
            # 'company':self.cleaned_data['company'],
        }
        custom_user = CustomUser.objects.create_user(
            context['email'],
            # context['firstname'],
            # context['lastname'],
            # context['company'],
            context['password']
        )

        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return custom_user

class CustomUserChangeForm(forms.ModelForm):##UserChangeForm
    """A form for updating users. Includes all the fields on
       the user, but replaces the password field with admin's
       disabled password hash display field.
       """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    # # firstname = forms.CharField(label = 'First Name', max_length = 120)
    # # lastname = forms.CharField(label = 'Last Name', max_length = 120)
    # email = forms.EmailField(label = 'New Email')
    # is_staff = forms.BooleanField(label='staff status', required=True)
    # # phone = PhoneNumberField()
    # old_password = forms.CharField(label = 'Current Password', min_length = 5, max_length = 50, widget = forms.PasswordInput)
    # new_password = forms.CharField(label = 'New Password', min_length = 5, max_length = 50, widget = forms.PasswordInput)
    # new_password2 = forms.CharField(label = 'Confirm New Password', min_length = 5, max_length = 50, widget = forms.PasswordInput)
    #
    # class Meta:
    #     model = CustomUser
    #     exclude = ['company', 'phone', 'firstname', 'last_name']
    #     # fields = ('email',)
    #
    # def clean_password(self):
    #     data = self.cleaned_data['password']
    #     # encrypt stuff
    #     return data
    #
    # # def clean_new_password(self):
    #
    #     # new_password = self.cleaned_data['new_password']
    #     # new_password2 = self.cleaned_data['new_password2']
    #     # if (new_password and new_password2) and (new_password != new_password2):
    #     #     raise ValidationError('Passwords do not match.')
    #     # if not (new_password and new_password2):
    #     #     raise ValidationError('Please enter new password twice.')
    #     #
    #     # return new_password
    #
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     email_list = CustomUser.objects.filter(email=email)
    #     if email_list.count():
    #         raise ValidationError('There is already an account associated with that email.')
    #
    #     return email

class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-basic'
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs['class'] = 'form-control datepicker'
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-time'
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs['class'] = 'form-control select2 select2-multiple'
            elif isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs['class'] = 'form-control select2'
            else:
                field.widget.attrs['class'] = 'form-control'

class SigninForm(StyleFormMixin, AuthenticationForm):
   pass

class SignupForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
        field_classes = {"username": UsernameField}
class UserSubscriptionForm(forms.ModelForm):

    class Meta:
        model = UserSubscription
        fields = '__all__'