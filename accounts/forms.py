from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignupModelForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(SignupModelForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileImageModelForm(forms.ModelForm):

    class Meta:
        """
        Telling django it is associated with Profile model
        """
        model = Profile
        """
        Set exclude attribute and render only image field
        """
        exclude = ('user', 'location', 'user_role',)

    # Override the default init method which allows the form to be customized
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Removed the form lables
        for field_name, field in self.fields.items():
            field.label = ""
        

class ProfileUpdateModelForm(forms.ModelForm):

    class Meta:
        """
        Telling django it is associated with Profile model
        """
        model = Profile
                        
        # Render all fields
        exclude = ('user',)

    # Override the default init method which allows the form to be customized
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Added placehoder to the form fields
        self.fields['location'].widget.attrs['placeholder'] = 'Add your location.'
        self.fields['user_role'].widget.attrs['placeholder'] = 'Add your profession.'

        # Removed the form lables
        for field_name, field in self.fields.items():
            field.label = ""
        