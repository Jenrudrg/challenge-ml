from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from admin_soft.models import Product, Sale


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        if not self.instance.pk:
            self.instance.created_user_id = self.request.user.id
        self.instance.modifier_user_id = self.request.user.id
        return super().save(commit)


class LoginForm(AuthenticationForm):
  username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
  password = forms.CharField(
      label=_("Password"),
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
  )


class ProductForm(BaseForm):
  class Meta:
    model = Product
    fields = ['name', 'description', 'price']
    widgets = {
      'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
      'description': forms.Textarea(attrs={"class": "form-control", "placeholder": "Description"}),
      'price': forms.NumberInput(attrs={"class": "form-control", "placeholder": "Price"}),
    }
