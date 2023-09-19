from django.contrib import admin
from .models import *

#class UserProfiles(admin.ModelAdmin):
    #list_display = ('title', 'id', 'count', 'price')
    #search_fields = ('title', )
    


admin.site.register(UserProfile)
admin.site.register(UserWall)
admin.site.register(UserPhotos)
admin.site.register(UserMusic)
admin.site.register(AllChat)
admin.site.register(Dialogs)
admin.site.register(HaveDialog)