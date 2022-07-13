from django.contrib import admin

from .models import Event, Choice, Attendee, AttendeeChoice


class EventAdmin(admin.ModelAdmin):
    readonly_fields = ["access_link"]


admin.site.register(Event, EventAdmin)
admin.site.register(Choice)
admin.site.register(Attendee)
admin.site.register(AttendeeChoice)
