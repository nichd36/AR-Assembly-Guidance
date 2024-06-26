

from django.urls import path
from .views import yolo_view

app_name = 'arweb'

urlpatterns = [
    path('yolo-view/<product_id>', yolo_view, name='yolo'),
]