"""
URL configuration for backend_solvro_alerts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView

from backend_solvro_alerts.views import index
from users.views import register, solvro_callback, solvro_login


@extend_schema(exclude=True)
class HiddenSpectacularAPIView(SpectacularAPIView):
    pass


urlpatterns = [
    path("", index, name="index"),
    path("admin/register/", register, name="admin_register"),
    path("admin/auth/solvro/login/", solvro_login, name="solvro_login"),
    path("admin/auth/solvro/callback/", solvro_callback, name="solvro_callback"),
    path("admin/", admin.site.urls),
    path("api/v1/", include("alerts.urls")),
    path("schema/", HiddenSpectacularAPIView.as_view(), name="schema"),
    path(
        "scalar/",
        TemplateView.as_view(template_name="scalar.html"),
        name="scalar-ui",
    ),
]
