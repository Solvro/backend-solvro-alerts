from django import forms
from django.contrib.auth.forms import UserCreationForm
from unfold.widgets import (
    UnfoldAdminEmailInputWidget,
    UnfoldAdminPasswordWidget,
    UnfoldAdminTextInputWidget,
)

from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=UnfoldAdminEmailInputWidget)
    first_name = forms.CharField(
        max_length=150, required=True, widget=UnfoldAdminTextInputWidget
    )
    last_name = forms.CharField(
        max_length=150, required=True, widget=UnfoldAdminTextInputWidget
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = UnfoldAdminPasswordWidget(
            attrs={"autocomplete": "new-password"}
        )
        self.fields["password2"].widget = UnfoldAdminPasswordWidget(
            attrs={"autocomplete": "new-password"}
        )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_active = False
        if commit:
            user.save()
        return user
