from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import password_validation
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required.")
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    profile_picture = forms.ImageField(required=False)
    age = forms.IntegerField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "profile_picture",
            "age",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize error messages for specific fields
        self.fields["username"].error_messages = {
            "required": "Please enter a valid username."
        }
        self.fields["email"].error_messages = {
            "required": "Please enter a valid email address."
        }
        self.fields["password1"].error_messages = {
            "required": "Please enter a valid password.",
            "min_length": "Password must contain at least 8 characters.",
        }
        self.fields["password2"].error_messages = {
            "required": "Please confirm your password."
        }
        self.fields["first_name"].error_messages = {
            "required": "Please enter your first name."
        }
        self.fields["last_name"].error_messages = {
            "required": "Please enter your last name."
        }
        self.fields["age"].error_messages = {"required": "Please enter your age."}


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
