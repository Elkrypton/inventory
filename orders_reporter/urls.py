from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import *


# router = routers.DefaultRouter()
# router.register(r'manufacturer_api', ManufacturerViewSet, basename="manufacturer_api")
# router.register(r'note_api', NoteViewSet, basename="feedback_api")
# router.register(r'search_api', SearchViewSet, basename="search_api")



urlpatterns = [

    ### Application front end routers
    path('', index, name='home'),


    path('graph/', GraphView,name='graph'),
    path('qr/<int:pk>/', generate_qr_code, name="product_qr"),
    path('myforms/', my_form_view, name='myforms'),
    path('export_excel/', export_inventory, name="export_excel"),
    path('list/',manufacturer_list, name='manufacturer_list'),
    path('delete/<int:pk>', delete_manufacturer, name="delete"),
    path("manufacturer/<int:pk>/pdf/", manufacturer_pdf, name="manufacturer_pdf"),

    path('manufacturer/<int:pk>/', manufacturer_detail, name='manufacturer_detail'),
    path('scan/',qrcode_scanner, name='scan'),
    path('search/',product_search, name="search"),
    path('feedback/',feedback, name="feedback"),
    path('submitted/', success_page, name="success_page"),
    path('edit_manufacturer/<int:pk>/', manufacturer_edit,name="edit")
    ]


if settings.DEBUG:
    
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        
