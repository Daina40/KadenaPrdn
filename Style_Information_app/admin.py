from django.contrib import admin
from .models import Customer, StyleInfo, StyleDescription

admin.site.register(Customer)
admin.site.register(StyleInfo)
admin.site.register(StyleDescription)
