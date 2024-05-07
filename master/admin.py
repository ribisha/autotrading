from django.contrib import admin
from . models import *

class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user_staff', 'staff_profile_image_display',) 
    def staff_profile_image_display(self, obj):
        return obj.staff_profile_image.url if obj.staff_profile_image else None
    staff_profile_image_display.short_description = 'static/images/angelone.png'  


admin.site.register(StaffProfile,StaffProfileAdmin)
admin.site.register(ClientProfile)
admin.site.register(FinanceProfile)

admin.site.register(MasterConnectAPI) 
admin.site.register(CreateRoom)
admin.site.register(MasterClientadd)