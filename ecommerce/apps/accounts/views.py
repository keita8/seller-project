from curses.ascii import US
from django.shortcuts import *
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.views import View
from .forms import *
from django.views.generic import *
from django.contrib.auth.decorators import login_required


class LoginPageView(TemplateView):
    template_name = "accounts/login.html"
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class()
        message = ""
        return render(
            request, self.template_name, context={"form": form, "message": message}
        )

    def post(self, request):
        form = self.form_class(request.POST)
        user = self.request
        if self.request.user.is_authenticated:
            return redirect('products:home')
        else:
            if form.is_valid():
                user = authenticate(
                    email=form.cleaned_data["email"], password=form.cleaned_data["password"]
                )
                next_url = request.POST.get("next")
                if user is not None:
                    login(request, user)
                    return redirect("products:home")
            else:
                messages.warning(request, "Adresse email ou mot de passe incorrect.")
                form = self.form_class(request.POST)
            return render(request, self.template_name, context={"form": form})


def register(request):
    form = RegisterForm
    if request.method == 'POST':
        form = RegisterForm
        if form.is_valid():
            form = RegisterForm(request.POST)
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password']
        else:
            form = RegisterForm(request.POST)
            
    template_name = "accounts/register.html"
    context = {
        'form': form
    }
    return render(request, template_name, context)


@login_required(login_url='accounts:login')
def logout_user(request):
    logout(request)
    messages.info(request, "Nous serons heureux de vous revoir !")
    return redirect("accounts:login")


def reset_password(request):
    reset_password_form = ResetPasswordForm
    if request.method == "POST":
        reset_password_form = ResetPasswordForm(request.POST or None)
        if reset_password_form.is_valid():
            email = reset_password_form.cleaned_data["email"]
            user = User.objects.get(email__iexact=email)
            if user.exists():
                print('adresse email existe')

    template_name = "accounts/reset.html"
    context = {
        'form': reset_password_form
    }
    return render(request, template_name, context)



@login_required(login_url='accounts:login')
def password_change(request):
    password_change_form = PasswordChangeForm
    user = User.objects.get(email__iexact=request.user)
    # return HttpResponse(user_password)
    if request.method == "POST":
        password_change_form = PasswordChangeForm(request.POST or None)
        if password_change_form.is_valid():
            current = password_change_form.cleaned_data.get("password")
            password1 = password_change_form.cleaned_data.get("password1")
            password2 = password_change_form.cleaned_data.get("password2")
            if password1 == password2:
                success = user.check_password(current)
                if success:
                    user.set_password(password1)
                    user.save()
                    logout(request)
                    messages.success(
                        request, "Votre mot de passe a été modifié avec succès."
                    )
                return redirect("accounts:login")
            else:
                messages.errors(request, "Les mots de passe ne correspondent pas")
                password_change_form = PasswordChangeForm()
    template_name = "accounts/password_change_form.html"
    context = {"password_change_form": password_change_form}
    return render(request, template_name, context)
