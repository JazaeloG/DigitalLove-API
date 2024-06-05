""" 
Configuración de URL para el proyecto digitalAPI.

La lista urlpatterns dirige las URL a las vistas.
Ejemplos: Vistas de función 
1. Añadir una importación: from my_app import views 
2. Añadir una URL a urlpatterns: path('', views.home, name='home') Vistas basadas en clases 
1. Añadir una importación: from other_app.views import Home 
2. Añadir una URL a urlpatterns: path('', Home.as_view(), name='home') Incluyendo otra configuración de URL 
1. Importar la función include(): from django.urls import include, path 
2. Añadir una URL a urlpatterns: path('blog/', include('blog.urls')) 

"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path ('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
