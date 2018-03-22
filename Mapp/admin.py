from django.contrib import admin
from .models import Album_table, Songs_table,Rating_table

admin.site.register(Album_table)
admin.site.register(Songs_table)
admin.site.register(Rating_table)

