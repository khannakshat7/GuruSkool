from django.contrib import admin
from classroom.models import ClassSlotBooking,ClassSlotDetails,GroupDiscussion,GroupDiscussionLinks
# Register your models here.

admin.site.register(ClassSlotBooking) # Registering ClassSlotBooking model
admin.site.register(ClassSlotDetails) # Registering ClassSlotDetails model
admin.site.register(GroupDiscussion) # Registering GroupDiscussion model
admin.site.register(GroupDiscussionLinks) # Registering GroupDiscussionLinks model