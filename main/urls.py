# main/urls.py
from django.urls import path
from .views import account_details_view, product_details_view, component_details_view, update_component_view, add_component, my_account_view

urlpatterns = [
        path('accounts/<email>', account_details_view, name="account_details_view"),
        path('products/<name>/<product_id>', product_details_view, name="product_details_view"),
        path('components/<name>/<component_id>', component_details_view, name="component_details_view"),
        path('update_components/<component_id>', update_component_view, name="update_component_view"),
        path('add_component', add_component, name="add_component"),
        path('my_account', my_account_view, name="my_account_view"),
]