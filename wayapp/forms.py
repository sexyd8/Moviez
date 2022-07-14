from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from .models import Profile, Membership
from django import forms


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields=('first_name', 'last_name', 'username', 'password1', 'password2')
        widgets = {
             'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
             'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
             'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
            #  'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
             'password1':forms.PasswordInput(attrs={'class':'form-control'}),
             'password2':forms.PasswordInput(attrs={'class':'form-control'}),
        }


class MemberForm(UserCreationForm):
    class Meta:
        model = User
        fields=('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'}),
    }



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=('first_name','title','dfee','last_name', 'phone', 'email')
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'Choose Membership Package'}),
            'dfee':forms.NumberInput(attrs={'class':'form-control','placeholder':'fee'}),
            # 'username':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}),
        }



class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields=('first_name', 'last_name', 'phone','fee')
        widgets = {
            'member':forms.TextInput(attrs={'class':'form-control','placeholder':'Member Package'}),
            'fee':forms.NumberInput(attrs={'class':'form-control','placeholder':'fee'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),
            # 'memeber_no':forms.TextInput(attrs={'class':'form-control','placeholder':'Gender'}),
        }



