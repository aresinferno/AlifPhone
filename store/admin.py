from django.contrib import admin
from django.contrib import admin
from .models import *
from django.urls import path
from django.http import JsonResponse


@admin.register(Brand)
class PartBrandAdmin(admin.ModelAdmin):
    pass

@admin.register(Type)
class PartTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Model)
class PartSeriesAdmin(admin.ModelAdmin):
    pass

@admin.register(Phone)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('type', 'brand', 'model')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("get-series/", self.admin_site.admin_view(self.get_series), name="get_series"),
        ]
        return custom_urls + urls

    def get_series(self, request):
        brand_id = request.GET.get("brand_id")
        series = Model.objects.filter(brand_id=brand_id).values("id", "name")

        return JsonResponse(list(series), safe=False)

    class Media:
        js = ("admin/js/dependent_dropdown.js",)

@admin.register(Place)
class PartPlaceAdmin(admin.ModelAdmin):
    pass
# Register your models here.
