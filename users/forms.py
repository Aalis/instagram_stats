# from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser


# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True, help_text="Required.")
#     first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
#     last_name = forms.CharField(max_length=30, required=True, help_text="Required.")
#     profile_picture = forms.ImageField(required=False)

#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = UserCreationForm.Meta.fields + (
#             "email",
#             "first_name",
#             "last_name",
#             "profile_picture",
#         )


# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = UserChangeForm.Meta.fields

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"required": "required"}),
        help_text="Required.",
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"required": "required"}),
        help_text="Required.",
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"required": "required"}),
        help_text="Required.",
    )
    profile_picture = forms.ImageField(required=False)

    # Custom error messages for form fields
    error_messages = {
        "password_mismatch": "The two password fields didn't match.",
        "invalid_email": "Please enter a valid email address.",
    }

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "profile_picture",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        # Check if the email is in a valid format
        if not email or not email.endswith(".com"):
            raise ValidationError(
                self.error_messages["invalid_email"],
                code="invalid_email",
            )

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )

        return password2


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
