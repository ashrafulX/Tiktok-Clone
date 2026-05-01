"""
URL configuration for _core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf.urls.static import static
from allauth.account.views import PasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/password/change/', PasswordChangeView.as_view(success_url = reverse_lazy('settings')),name="account_change_password"),
    path('accounts/', include('allauth.urls')),
    path('',include('_posts.urls')),
    path('',include('_users.urls')),
    path('following/',include('_network.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        ]