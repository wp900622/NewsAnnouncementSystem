from django.contrib import admin

# Register your models here.
from myapp.models import newsunit

class newsunitAdmin(admin.ModelAdmin):
    list_display = ('id','Catego',)

admin.site.register(newsunit)
