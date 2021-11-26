from django.db import models

# Class slot details model to store information about the class slots
class ClassSlotDetails(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    link = models.URLField(max_length=200, blank=True)
    max_capacity = models.IntegerField(default=30)
    current_capacity = models.IntegerField(default=30)

    def __str__(self):
        return self.name


# Class slot booking model to store information about the class slots and user who booked it
class ClassSlotBooking(models.Model):
    class_details = models.ForeignKey(
        ClassSlotDetails, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.class_details.name


# Group Discussion slot details model to store information about the GD slots
class GroupDiscussion(models.Model):
    topic = models.CharField(max_length=100)
    number_of_groups = models.IntegerField(default=1)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.topic


# Group Discussion links model to save the links of the GD slots
class GroupDiscussionLinks(models.Model):
    group_discussion = models.ForeignKey(
        GroupDiscussion, on_delete=models.CASCADE)
    link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.group_discussion.topic
