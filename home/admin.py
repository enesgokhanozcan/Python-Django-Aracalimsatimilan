from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactFormMessage

class ContactForMessageAdmin(admin.ModelAdmin):
    list_display = ['name','email','subject','note','status']
    readonly_fields = ('name', 'subject', 'email', 'message', 'ip')
    list_filter = ['status']

admin.site.register(ContactFormMessage,ContactForMessageAdmin)
admin.site.register(Setting)


