from django.urls import path
from .views import mainPageView, addDataView, authView,editView,addPDFView, allDataView, deleteDataView,LogoutView,exportView,LoginView,RegisterView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',mainPageView, name = 'main'),
    path('add',addDataView, name = 'addData'),
    path('addPDF', addPDFView, name='addPDF'),
    path('edit/<int:pk>', editView, name='edit'),
    path('allData/<int:pk>', allDataView, name='allData'),
    path('deleteData/<int:pk>', deleteDataView, name='deleteData'),
    path('exportData/<str:pk>', exportView, name='exportData'),
    path('login', LoginView.as_view(), name="login"),
    path('register', RegisterView.as_view(), name="register"),
    path('logout', LogoutView.as_view(next_page='/'), name='logout'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
