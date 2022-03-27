from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import (handler400, handler403, handler404, handler500)


handler404 = 'main.views.custom_page_not_found_view'
handler500 = 'main.views.custom_error_view'
handler403 = 'main.views.custom_permission_denied_view'
handler400 = 'main.views.custom_bad_request_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)