from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
    path('add',include('app.urls')),
    path('addPDF', include('app.urls')),
    path('auth', include('app.urls')),
    path('edit', include('app.urls')),
    path('login', include('app.urls')),
    path('register', include('app.urls')),
    path('logout', include('app.urls'))


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

