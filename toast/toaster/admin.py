from django.contrib import admin
from .models import Toaster
# Register your models here.

class ToasterAdmin(admin.ModelAdmin):  
    list_display = ('name', 'income', 'age') 

# Register your models here.
admin.site.register(Toaster, ToasterAdmin)