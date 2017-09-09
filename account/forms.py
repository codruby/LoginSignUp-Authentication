from django import forms
from .models import AppUser


class RegisterForm(forms.ModelForm):
    def clean_fistname(self):
        firstname = self.cleaned_data['first_name']
        return firstname

    def clean_middlename(self):
        middlename = self.cleaned_data['middle_name']
        return middlename

    def clean_lastname(self):
        lastname = self.cleaned_data['last_name']
        return lastname

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6 or len(password) > 14:
            raise forms.ValidationError('Password must be between 6 and 14 characters', code='invalid_length', )
        return password

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if AppUser.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError('Mobile number already in use', code='mobile_exists')
        return mobile

    def clean_email(self):
        email = self.cleaned_data['email']
        if AppUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address already in use', code='email_exists')
        return email

    class Meta:
        model = AppUser
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'mobile', 'password']


# class ForgetPassword(forms.ModelForm):
#
#     def clean_password(self):
#         password = self.cleaned_data['password']
#         if len(password) < 6 or len(password) > 14:
#             raise forms.ValidationError('Password must be between 6 and 14 characters', code='invalid_length', )
#         return password
#
#     class Meta:
#         model = AppUser
#         fields = ['email', 'password']
