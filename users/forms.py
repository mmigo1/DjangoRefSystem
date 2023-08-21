from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('phone',)


class CustomUserChangeForm(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(
                f"../../{self.instance.pk}/password/"
            )
        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                "content_type"
            )

    class Meta:
        model = CustomUser
        fields = ('phone',)


class RegisterForm(forms.Form):
    phone = forms.CharField(label="Enter your phone number here")

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        user_details = CustomUser.objects.filter(phone=phone)
        if user_details.exists():
            raise forms.ValidationError(
                "An account with this phone number already exists! Please try registering using a different phone number or try logging in!")
        return phone

    class Meta:
        model = CustomUser
        fields = ('phone',)
