from django.contrib import admin
from .models import *
# Register your models here.

class Date(admin.ModelAdmin):
    readonly_fields = ('Created','updated',)

admin.site.register(User_info)
admin.site.register(genre,Date)
admin.site.register(song)
admin.site.register(add_play_list)


