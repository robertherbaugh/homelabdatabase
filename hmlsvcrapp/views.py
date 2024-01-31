from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Server, Service, Network, Credential, UptimeKumaMonitors
from .forms import NetworkForm, ServiceForm, ServerForm, CredentialForm, UserProfileForm, CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy

def index(request):
    return render(request, 'hmlsvcrapp/index.html', {'current_page': 'home'})

def server_list(request):
    servers = Server.objects.all().prefetch_related('cred_name')
    return render(request, 'hmlsvcrapp/server_list.html', {'servers': servers, 'current_page': 'Servers'})

def service_list(request):
    services = Service.objects.all().prefetch_related('credentials')
    return render(request, 'hmlsvcrapp/service_list.html', {'services': services, 'current_page': 'Services'})

def network_list(request):
    networks = Network.objects.all()
    return render(request, 'hmlsvcrapp/network_list.html', {'networks': networks, 'current_page': 'Networks'})

def credential_list(request):
    credentials = Credential.objects.prefetch_related('servercredential_set__server', 'servicecredential_set__service')
    return render(request, 'hmlsvcrapp/credential_list.html', {'credentials': credentials, 'current_page': 'Credentials'})

def list_monitors(request):
    monitors = UptimeKumaMonitors.objects.all()
    return render(request, 'monitors_list.html', {'monitors': monitors})

# Network Manipulation
@login_required
def add_network(request):
    if request.method == 'POST':
        form = NetworkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Network added successfully.')
            return redirect('network_list')
    else:
        form = NetworkForm()
    return render(request, 'hmlsvcrapp/add_network.html', {'form': form})

@login_required
def edit_network(request, network_id):
    network = get_object_or_404(Network, pk=network_id)
    if request.method == 'POST':
        form = NetworkForm(request.POST, instance=network)
        if form.is_valid():
            form.save()
            return redirect('network_list')
    else:
        form = NetworkForm(instance=network)
    return render(request, 'hmlsvcrapp/edit_network.html', {'form': form})

@login_required
def delete_network(request, network_id):
    if request.user.has_perm('hmlsvcrapp.delete_network'):
        network = get_object_or_404(Network, pk=network_id)
        network.delete()
        messages.success(request, 'Network deleted successfully.')
        return redirect('network_list')
    else:
        messages.error(request, 'You do not have permission to delete this network.')
        return redirect('network_list')

# Services Manipulation
@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully.')
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'hmlsvcrapp/add_service.html', {'form': form})

@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'hmlsvcrapp/edit_service.html', {'form': form})

@login_required
def delete_service(request, service_id):
    if request.user.has_perm('hmlsvcrapp.delete_service'):
        service = get_object_or_404(Service, pk=service_id)
        service.delete()
        messages.success(request, 'Service deleted successfully.')
        return redirect('service_list')
    else:
        messages.error(request, 'You do not have permission to delete this service.')
        return redirect('service_list')

@login_required
def decommission_service(request, service_id):
    if request.user.has_perm('hmlsvcrapp.change_service'):
        service = get_object_or_404(Service, pk=service_id)

        # Toggle the service status between 'Active' and 'Decommissioned'
        if service.status == 'Decommissioned':
            service.status = 'Active'
            action = 'reactivated'
        else:
            service.status = 'Decommissioned'
            action = 'decommissioned'

        service.save()
        messages.success(request, f'Service {service.name} has been {action}.')

        # Redirect back to the previous page or to the service list
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'service_list'))
    else:
        messages.error(request, 'You do not have permission to change this service.')
        return redirect('service_list')


@login_required
def add_server(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Server added successfully.')
            return redirect('server_list')
    else:
        form = ServerForm()
    return render(request, 'hmlsvcrapp/add_server.html', {'form': form})

# Server Manipulation
@login_required
def edit_server(request, server_id):
    server = get_object_or_404(Server, pk=server_id)
    if request.method == 'POST':
        form = ServerForm(request.POST, instance=server)
        if form.is_valid():
            form.save()
            messages.success(request, 'Server updated successfully.')
            return redirect('server_list')
    else:
        form = ServerForm(instance=server)
    return render(request, 'hmlsvcrapp/edit_server.html', {'form': form})

@login_required
def delete_server(request, server_id):
    if request.user.has_perm('hmlsvcrapp.delete_server'):
        server = get_object_or_404(Server, pk=server_id)
        server.delete()
        messages.success(request, 'Server deleted successfully.')
        return redirect('server_list')
    else:
        messages.error(request, 'You do not have permission to delete this server.')
        return redirect('server_list')

#@login_required
#def deactivate_server(request, server_id):
#    if request.user.is_superuser or request.user.has_perm('hmlsvcrapp.edit_server'):
#        server = get_object_or_404(Server, pk=server_id)
#        server.is_active = not server.is_active  # Toggle the is_active status
#        server.save()
#
#        action = "reactivated" if server.is_active else "deactivated"
#        messages.success(request, f"The server with ID {server_id} has been {action}.")
#        return redirect('server_list')
#    else:
#        messages.error(request, 'You do not have permission to change this server\'s status.')
#        return redirect('server_list')

# Credentials manipulation
@login_required
def add_credential(request):
    if request.method == 'POST':
        form = CredentialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Credential added successfully.')
            return redirect('credential_list')
    else:
        form = CredentialForm()
    return render(request, 'hmlsvcrapp/add_credential.html', {'form': form})

@login_required
def edit_credential(request, credential_id):
    credential = get_object_or_404(Credential, pk=credential_id)
    if request.method == 'POST':
        form = CredentialForm(request.POST, instance=credential)
        if form.is_valid():
            form.save()
            messages.success(request, 'Credential updated successfully.')
            return redirect('credential_list')
    else:
        form = CredentialForm(instance=credential)
    return render(request, 'hmlsvcrapp/edit_credential.html', {'form': form})

@login_required
def delete_credential(request, credential_id):
    if request.user.has_perm('hmlsvcrapp.delete_credential'):
        credential = get_object_or_404(Credential, pk=credential_id)
        credential.delete()
        messages.success(request, 'Credential deleted successfully.')
        return redirect('credential_list')
    else:
        messages.error(request, 'You do not have permission to delete this credential.')
        return redirect('credential_list')

# User manipulation
@login_required
def edit_user_profile(request, user_id):
    # Ensure 'user_to_edit' is defined here
    user_to_edit = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user_to_edit, current_user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('index')  # Replace with your success URL
        else:
            print(form.errors)  # Add this for debugging
            messages.error(request, "Error updating profile.")
    else:
        form = CustomUserChangeForm(instance=user_to_edit, current_user=request.user)

    # Make sure 'user_to_edit' is included in the context
    return render(request, 'hmlsvcrapp/edit_user_profile.html', {'form': form, 'user_to_edit': user_to_edit})

@login_required
def edit_profile(request, user_id):
    user_to_edit = get_object_or_404(User, pk=user_id)

    # Initialize the form either with POST data or as a blank form
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user_to_edit, current_user=request.user)
    else:
        form = CustomUserChangeForm(instance=user_to_edit, current_user=request.user)

    # Allow superusers or staff to edit any profile, but regular users can only edit their own
    if not (request.user.is_superuser or request.user.is_staff) and request.user != user_to_edit:
        messages.error(request, "You are not allowed to edit this user.")
        return redirect('index')

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f"Profile for {user_to_edit.username} updated successfully.")
            return redirect('user_list')
        else:
            print(form.errors)  # Add this for debugging
            messages.error(request, f"Profile for {user_to_edit.username} could not be updated.")
            #return redirect('user_list')

    return render(request, 'hmlsvcrapp/edit_profile.html', {
        'form': form, 
        'user_to_edit': user_to_edit, 
        'username_being_edited': user_to_edit.username
    })


@login_required
class CustomPasswordChangeView(generic.UpdateView):
    template_name = 'edit_password.html'
    success_url = reverse_lazy('password_change_done')
    # Your form and view logic here

@login_required
def user_list(request):
    # Check if the user is staff or superuser
    if request.user.is_superuser or request.user.is_staff:
        # If so, fetch all user accounts
        users = User.objects.all()
    else:
        # Otherwise, only fetch the logged-in user's account
        users = User.objects.filter(id=request.user.id)

    # Render the template with the users context
    return render(request, 'hmlsvcrapp/user_list.html', {'users': users})

@login_required
def delete_user(request, user_id):
    if request.user.has_perm('auth.delete_user'):  # Update the permission
        user = get_object_or_404(User, pk=user_id)  # Get the user object
        if user != request.user:  # Prevent the user from deleting themselves
            user.delete()
            messages.success(request, 'User deleted successfully.')
        else:
            messages.error(request, 'You cannot delete your own account.')
    else:
        messages.error(request, 'You do not have permission to delete this user.')

    return redirect('user_list')  # Redirect to the user list page

@login_required
@permission_required('auth.add_user', raise_exception=True)
def add_user_django(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to user list or any other page
            return redirect('user_list')
    else:
        form = UserCreationForm()

    return render(request, 'hmlsvcrapp/add_user.html', {'form': form})

@login_required
def add_user(request):
    if not (request.user.is_superuser or request.user.is_staff):
        return HttpResponseForbidden("You do not have permission to access this page.")

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, current_user=request.user)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, f"New user '{new_user.username}' was successfully created.")
            return redirect('user_list')
    else:
        form = CustomUserCreationForm(current_user=request.user)

    return render(request, 'hmlsvcrapp/add_user.html', {'form': form})

@login_required
def deactivate_user(request, user_id):
    user_to_toggle = get_object_or_404(User, pk=user_id)

    # Prevent staff from toggling a superuser's active status
    if user_to_toggle.is_superuser and not request.user.is_superuser:
        messages.error(request, "You do not have permission to change a superuser's active status.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'user_list'))

    # Prevent self-deactivation
    if request.user.id == user_id:
        messages.error(request, "You cannot deactivate your own account.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'user_list'))

    if request.user.is_superuser or request.user.is_staff:
        # Toggle the is_active status
        user_to_toggle.is_active = not user_to_toggle.is_active
        user_to_toggle.save()

        action = "reactivated" if user_to_toggle.is_active else "deactivated"
        messages.success(request, f"The user {user_to_toggle.username} has been {action}.")
    else:
        messages.error(request, "You do not have permission to change this user's active status.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'user_list'))

class CustomLoginView(LoginView):
    template_name = 'hmlsvcrapp/login.html'

    def form_invalid(self, form):
        # Attempt to authenticate the user
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and not user.is_active:
            # User is valid, but the account is inactive
            messages.error(self.request, "Your account is disabled. Please contact the administrator.")
        else:
            # Generic login failure message
            messages.error(self.request, "Login failed. Please check your username and password.")

        return super().form_invalid(form)

@user_passes_test(lambda u: u.is_superuser)
def edit_superuser_profile(request, user_id):
    # Ensure 'user_to_edit' is defined here
    user_to_edit = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user_to_edit, current_user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('index')  # Replace with your success URL
        else:
            print(form.errors)  # Add this for debugging
            messages.error(request, "Error updating profile.")
    else:
        form = CustomUserChangeForm(instance=user_to_edit, current_user=request.user)

    # Make sure 'user_to_edit' is included in the context
    return render(request, 'hmlsvcrapp/edit_superuser_profile.html', context, {'form': form, 'user_to_edit': user_to_edit})
    #return render(request, 'edit_superuser_profile.html', context)

@user_passes_test(lambda u: u.is_staff)
def edit_staff_profile(request, user_id):
    user_to_edit = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user_to_edit, current_user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('index')  # Adjust redirect as needed
        else:
            messages.error(request, "Error updating profile.")
    else:
        form = CustomUserChangeForm(instance=user_to_edit, current_user=request.user)

    return render(request, 'hmlsvcrapp/edit_staff_profile.html', {'form': form, 'user_to_edit': user_to_edit})

@login_required
def edit_user_profile(request):
    user_to_edit = request.user  # User edits their own profile

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user_to_edit, current_user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('index')
        else:
            messages.error(request, "Error updating profile.")
    else:
        form = CustomUserChangeForm(instance=user_to_edit, current_user=request.user)

    return render(request, 'hmlsvcrapp/edit_user_profile.html', {'form': form, 'user_to_edit': user_to_edit})

class AdminPasswordResetView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = User
    template_name = 'hmlsvcrapp/admin_password_reset.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('user_list')

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')
        return User.objects.get(pk=user_id)

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # SetPasswordForm does not take 'instance' parameter, so remove it.
        kwargs.pop('instance', None)
        kwargs['user'] = self.get_object()  # Pass the user instance to the form
        return kwargs

    def form_valid(self, form):
        user = self.get_object()
        response = super().form_valid(form)
        messages.success(self.request, f"Password for '{user.username}' has been successfully updated.")
        return response

    def form_invalid(self, form):
        user = self.get_object()
        messages.error(self.request, f"Failed to update the password for '{user.username}'. Please check the form for errors.")
        return super().form_invalid(form)

class ToggleStaffStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # Allow only superusers to access this view
        return self.request.user.is_superuser or self.request.user.is_staff

    def post(self, request, user_id):
        user_to_toggle = get_object_or_404(User, pk=user_id)

        # Prevent non-superusers from editing superusers
        if user_to_toggle.is_superuser and not request.user.is_superuser:
            messages.error(request, "You do not have permission to edit a superuser.")
            return redirect('user_list')  # Adjust the redirect as needed

        user_to_toggle.is_staff = not user_to_toggle.is_staff
        user_to_toggle.save()

        action = "promoted to" if user_to_toggle.is_staff else "demoted from"
        messages.success(request, f"User {user_to_toggle.username} has been {action} staff.")
        return redirect('user_list')  # Adjust the redirect as needed

# List out Details for AJAX Calls
def get_network_details(request, network_id):
    try:
        network = Network.objects.get(pk=network_id)
        data = {
            'name': network.name,
            'vlan_id': network.vlan_id,
            'subnet_mask': network.subnet_mask,
            'ip_space': network.ip_space,
            # add other network details you want to include
        }
        return JsonResponse(data)
    except Network.DoesNotExist:
        return JsonResponse({'error': 'Network not found'}, status=404)

def get_server_details(request, server_id):
    try:
        server = Server.objects.get(pk=server_id)
        network_name = server.network.name if server.network else None

        data = {
            'name': server.name,
            'ip_address': server.ip_address,
            'network': network_name,  # Directly assign the network name
            'type': server.type,
            'location': server.location,
            'description': server.description,
            # Include other details as needed
        }
        return JsonResponse(data)
    except Server.DoesNotExist:
        return JsonResponse({'error': 'Server not found'}, status=404)

