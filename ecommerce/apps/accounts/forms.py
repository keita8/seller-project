from xml.dom import ValidationErr
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

User = get_user_model()

class RegisterForm(forms.ModelForm):
    """
    The default 

    """

    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    # password_2 = forms.CharField(label='Confirmez votre mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("adresse email déjà associée à un autre compte")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and len(password) < 8:
            raise ValidationError("Mot de passe maximum (8) caractères.")
        return cleaned_data


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirmez votre mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]





class UserLoginForm(forms.Form):
    """UserLoginForm definition."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Votre adresse email",
                "class": "input-field",
                "maxlenght": 255,
                "id": "email",
                "name": "email",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Votre mot de passe",
                "class": "input-field",
                "id": "password",
                "name": "password",
            }
        ),
    )

    # class Meta:
    #     model = User
    #     fields = ("email", "password")

    def clean_email(self):
        """
        Verify email is available.
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if not qs.exists():
            raise forms.ValidationError(
                "Cette adresse email n'est associée à un aucun compte"
            )
        return email




class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Votre adresse email",
                "class": "input-field",
                "maxlenght": 255,
                "id": "email",
                "name": "email",
            }
        ),
    )

    def clean_email(self):
        """
        Verify email is available.
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if not qs.exists():
            raise forms.ValidationError(
                "Cette adresse email n'est associée à un aucun compte"
            )
        return email


class PasswordChangeForm(forms.Form):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Votre mot de passe actuel",
                "class": "input-field",
                "id": "password",
                "name": "password",
            }
        ),
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Votre nouveau mot de passe",
                "class": "input-field",
                "id": "password",
                "name": "password1",
            }
        ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmez votre mot de passe",
                "class": "input-field",
                "id": "password",
                "name": "password2",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

