from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, "Account created successfully. You can now log in."
        )
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, "There was an error creating your account. Please try again."
        )
        return response


# from django.contrib import messages
# from django.urls import reverse_lazy
# from django.views.generic import CreateView
# from .forms import CustomUserCreationForm


# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"
