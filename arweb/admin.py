from django.contrib import admin
from arweb.models import Product, Step, Component

# Register your models here.
class StepAdmin(admin.ModelAdmin):
    list_display = ["title", "product", "order"]
    ordering = ["order"]
    list_filter = ["product"]
admin.site.register(Step, StepAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ["preview_name", "preview_desc", "created_at", "updated_at"]
admin.site.register(Product, ProductAdmin)

class ComponentAdmin(admin.ModelAdmin):
    model = Component
    list_display = ["name", "component_id"]
admin.site.register(Component, ComponentAdmin)