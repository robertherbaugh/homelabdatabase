from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib import admin
from .views import CustomLoginView, ToggleStaffStatusView, get_network_details, get_server_details
from hmlsvcrapp.views import AdminPasswordResetView

urlpatterns = [
    path('servers/', views.server_list, name='server_list'),
    path('services/', views.service_list, name='service_list'),
    path('networks/', views.network_list, name='network_list'),
    path('credentials/', views.credential_list, name='credential_list'),
    path('', views.index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', RedirectView.as_view(url='/hmlsvcrapp/', permanent=True)),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('networks/<int:network_id>/edit/', views.edit_network, name='edit_network'),
    path('add_network/', views.add_network, name='add_network'),
    path('networks/<int:network_id>/delete/', views.delete_network, name='delete_network'),
    path('add_service/', views.add_service, name='add_service'),
    path('services/<int:service_id>/delete/', views.delete_service, name='delete_service'),
    path('services/<int:service_id>/edit/', views.edit_service, name='edit_service'),
    path('add_server/', views.add_server, name='add_server'),
    path('servers/<int:server_id>/delete/', views.delete_server, name='delete_server'),
    path('servers/<int:server_id>/edit/', views.edit_server, name='edit_server'),
    path('services/<int:service_id>/decommission/', views.decommission_service, name='decommission_service'),
    path('add_credential/', views.add_credential, name='add_credential'),
    path('credentials/<int:credential_id>/edit/', views.edit_credential, name='edit_credential'),
    path('credentials/<int:credential_id>/delete/', views.delete_credential, name='delete_credential'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('admin/', admin.site.urls),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    #path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),
    path('edit_user_profile/<int:user_id>', views.edit_user_profile, name='edit_user_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='hmlsvcrapp/edit_password.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='hmlsvcrapp/password_change_done.html'), name='password_change_done'),
    path('users/', views.user_list, name='user_list'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('edit/profile/<int:user_id>/deactivate/', views.deactivate_user, name='deactivate_user'),
    path('edit/superuser/<int:user_id>/', views.edit_superuser_profile, name='edit_superuser_profile'),
    path('edit/staff/<int:user_id>/', views.edit_staff_profile, name='edit_staff_profile'),
    path('edit/profile/', views.edit_user_profile, name='edit_user_profile'),
    path('edit/users/<int:user_id>/reset-password/', AdminPasswordResetView.as_view(), name='admin_password_reset'),
    path('edit/users/<int:user_id>/toggle-staff/', ToggleStaffStatusView.as_view(), name='toggle_staff_status'),
    path('get-network-details/<int:network_id>/', get_network_details, name='get_network_details'),
    path('get-server-details/<int:server_id>/', get_server_details, name='get_server_details'),
    #path('networks/<int:network_id>/edit/', views.edit_network, name='hmlsvcrapp_network_change'),
    # other URL patterns...
    # Add other URL patterns here
]
