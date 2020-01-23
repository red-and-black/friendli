import re

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import (
    get_password_validators,
    validate_password,
)
from .models import (
    PersonalInterest,
    ProfessionalInterest,
    Language,
    LookingFor,
    Profile,
)


class LoginForm(forms.Form):
    username = forms.CharField(
        label='User name or email',
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )


def personal_interest_choices():
    personal_interests = PersonalInterest.objects.all()

    return [(pi.pk, pi.personal_interest) for pi in personal_interests]


def prof_interest_choices():
    professional_interests = ProfessionalInterest.objects.all()

    return [(pi.pk, pi.prof_interest) for pi in professional_interests]


def language_choices():
    languages = Language.objects.all()

    return [(i.pk, i.language) for i in languages]


def looking_for_choices():
    looking_fors = LookingFor.objects.all()
    return [(i.pk, i.looking_for) for i in looking_fors]


class ProfileSearchForm(forms.Form):
    personal_interests = forms.MultipleChoiceField(
        choices=personal_interest_choices,
        required=False,
    )
    prof_interests = forms.MultipleChoiceField(
        choices=prof_interest_choices,
        required=False,
    )
    languages = forms.MultipleChoiceField(
        choices=language_choices,
        required=False,
    )
    looking_for = forms.MultipleChoiceField(
        choices=looking_for_choices,
        required=False,
    )
    detail = forms.CharField(
        required=False
    )
    stack = forms.CharField(
        required=False
    )


class UserSearchForm(forms.Form):
    username = forms.CharField(
        required=False
    )


class LanguageForm(forms.ModelForm):
    """
    A form to add, remove or edit the languages available to users for their
    profiles.
    """

    class Meta:
        model = Language
        fields = ('language',)


class LookingForForm(forms.ModelForm):
    """
    A form to add, remove or edit the looking_for options available to users
    for their profiles.
    """

    class Meta:
        model = LookingFor
        fields = ('looking_for',)


class ProfInterestForm(forms.ModelForm):
    """
    A form to add, remove or edit the interests available to users for their
    profiles.
    """

    class Meta:
        model = ProfessionalInterest
        fields = ('prof_interest',)


class PersonalInterestForm(forms.ModelForm):
    """
    A form to add, remove or edit the interests available to users for their
    profiles.
    """

    class Meta:
        model = PersonalInterest
        fields = ('personal_interest',)


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def clean_username(self):
        # Usernames can be no longer than 15 characters
        username = self.cleaned_data['username']
        if len(username) > 15:
            error_msg = "A username can't have more than 15 characters"
            raise forms.ValidationError(error_msg)

        # Usernames must be ASCII
        regex = r'^[a-zA-Z0-9_-]*$'
        username_regex = re.compile(regex)
        if not username_regex.match(username):
            error_msg = (
                "A username can only include ASCII letters, numerals, -, and _"
            )
            raise forms.ValidationError(error_msg)

        # Usernames must be case-insensitive unique.
        another_user_has_that_username = User.objects.\
            filter(username__iexact=username).\
            exclude(username__iexact=self.instance.username).\
            exists()
        if another_user_has_that_username:
            error_msg = "That username is unavailable."
            raise forms.ValidationError(error_msg)

        return username


class AddUserForm(forms.ModelForm):
    """
    A form that creates a user.
    """
    password2 = forms.CharField(widget=forms.PasswordInput())
    terms = forms.BooleanField(widget=forms.CheckboxInput())
    privacy = forms.BooleanField(widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
        )
        widgets = {'password': forms.PasswordInput()}

    def clean_username(self):
        # Usernames can be no longer than 16 characters
        username = self.cleaned_data['username']
        if len(username) > 16:
            error_msg = "A username can't have more than 16 characters"
            raise forms.ValidationError(error_msg)

        # Usernames must be ASCII
        regex = r'^[a-zA-Z0-9_-]*$'
        username_regex = re.compile(regex)
        if not username_regex.match(username):
            error_msg = (
                "A username can only include ASCII letters, numerals, -, and _"
            )
            raise forms.ValidationError(error_msg)

        # Usernames must be case-insensitive unique.
        if User.objects.filter(username__iexact=username).exists():
            error_msg = "That username is unavailable."
            raise forms.ValidationError(error_msg)

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        validators = get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
        validate_password(password, password_validators=validators)

        return password

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            error_msg = "The two password fields didn't match."
            raise forms.ValidationError(error_msg)

        return password


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'detail',
            'stack',
            'github',
            'twitter',
            'prof_interests',
            'personal_interests',
            'languages',
            'looking_for',
        )
        widgets = {
            'stack': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_github(self):
        github = self.cleaned_data.get("github")
        # Remove any leading @ characters.
        while github.startswith('@'):
            github = github[1:]

        return github

    def clean_twitter(self):
        twitter = self.cleaned_data.get("twitter")
        # Remove any leading @ characters.
        while twitter.startswith('@'):
            twitter = twitter[1:]

        return twitter
