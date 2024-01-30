from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from hmlsvcrapp.views import AdminPasswordResetView  # Import the view here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hmlsvcrapp/', include('hmlsvcrapp.urls')),
    path('', RedirectView.as_view(url='/hmlsvcrapp/', permanent=True)),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
]
