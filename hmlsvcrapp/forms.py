from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import Network, Service, Server, Credential
from django.contrib.auth.views import LoginView

class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = '__all__'  # Include all fields from the Network model
        # If you want to include specific fields only, list them like ['name', 'ip_space', ...]

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        #fields = ['server', 'name', 'port', 'status', 'ip', 'wazuh_agent_installed', 'fqdn', 'cloudflare_proxy_configured', 'reverse_proxy_configured', 'ldn', 'dns_configured', 'credentials']

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = '__all__'  

class CredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = '__all__'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        #fields = ['first_name', 'last_name', 'email']  # Add other fields you need

class CustomUserChangeForm(UserChangeForm):
    is_active = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('current_user', None)
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)

        # Conditionally remove the is_superuser field for non-superusers
        if not user.is_superuser:
            self.fields.pop('is_superuser')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']

    def save(self, commit=True):
        user = super().save(commit=False)

        # Only update fields if they are present in the form
        if 'is_active' in self.cleaned_data:
            user.is_active = self.cleaned_data['is_active']
        if 'is_staff' in self.cleaned_data:
            user.is_staff = self.cleaned_data['is_staff']
        if 'is_superuser' in self.cleaned_data:
            user.is_superuser = self.cleaned_data['is_superuser']

        if commit:
            user.save()
            self.save_m2m()  # Save many-to-many fields like groups and permissions

        return user

class CustomUserCreationForm(UserCreationForm):
    is_active = forms.BooleanField(initial=True, required=False)
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('current_user', None)
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields.pop('is_superuser')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = self.cleaned_data["is_active"]
        user.is_staff = self.cleaned_data["is_staff"]
        if 'is_superuser' in self.cleaned_data:
            user.is_superuser = self.cleaned_data["is_superuser"]
        if commit:
            user.save()
        return user