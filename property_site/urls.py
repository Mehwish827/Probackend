from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from plots.views import OtherPlotViewSet
from plots.views import create_dealer
router = DefaultRouter()
router.register(r'other-plots', OtherPlotViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plots.urls')),
    path('', include(router.urls)),
    path('create-dealer/', create_dealer, name='create-dealer'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
