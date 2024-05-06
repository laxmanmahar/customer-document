from django.contrib import admin

# Register your models here.
from UserApp import models as UserAppModel

admin.site.register(UserAppModel.Country)
admin.site.register(UserAppModel.DocumentSet)
admin.site.register(UserAppModel.Customer)
admin.site.register(UserAppModel.CustomeUser)
admin.site.register(UserAppModel.FileUpload)
