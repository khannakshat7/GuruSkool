from django.contrib import admin
from classroom.models import ClassSlotBooking,ClassSlotDetails,GroupDiscussion,GroupDiscussionLinks
# Register your models here.

admin.site.register(ClassSlotBooking)
admin.site.register(ClassSlotDetails)
admin.site.register(GroupDiscussion)
admin.site.register(GroupDiscussionLinks)