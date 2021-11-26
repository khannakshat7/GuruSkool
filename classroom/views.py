import random
import string
import pandas
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from classroom.forms import UserForm
from django.contrib.auth.decorators import login_required, permission_required
from classroom.models import ClassSlotBooking, ClassSlotDetails, GroupDiscussionLinks, GroupDiscussion

# This view is used to handle root url request and redirect to home page
def index(request):
    # user = request.user
    # if user.is_superuser:
    #     return redirect('')
    # elif user.is_authenticated:
    #     return redirect('')
    # else:
    return render(request, 'index.html')


# This view is used to handle register url request and redirect to registration page
def register(request):
    return render(request, 'register.html')


# This view is used to handle registration of faculty and get all data from register form and save the user in the DB
def teacherRegister(request):
    registeredcheck = False
    if(request.method == 'POST'):
        user_form = UserForm(data=request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if user_form.is_valid():
            user = user_form.save()
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(user.password)
            user.is_staff = True
            user.is_superuser = True  # Faculty permission is set to true
            user.save()  # User(faculty) is saved in the DB
            registeredcheck = True
            msg = {"message": True}
            # Redirect to login page if registration is successful
            return render(request, "login.html", msg)
        else:
            error = {"error": True}
            # Redirect to register page if registration is unsuccessful
            return render(request, "register.html", error)
    else:
        return render(request, 'register.html')


# This view is used to handle registration of student and get all data from register form and save the user in the DB
def studentRegister(request):
    registeredcheck = False
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    if(request.method == 'POST'):
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(user.password)
            user.is_staff = False
            user.is_superuser = False  # Faculty permission is set to false as it is a Student
            user.save()  # User(student) is saved in the DB
            registeredcheck = True
            msg = {"message": True}
            # Redirect to login page if registration is successful
            return render(request, "login.html", msg)
        else:
            error = {"error": True}
            # Redirect to register page if registration is unsuccessful
            return render(request, "register.html", error)
    else:
        return render(request, 'register.html')


# This view is used to handle login url request and login user if the credentials are correct
def loginUser(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')  # Get username from login form
        password = request.POST.get('password')  # Get password from login form
        # Authenticate user
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)  # Login user
                # if(user.is_superuser):
                #     return redirect('/slot/') # Redirect to home page if user is a faculty
                # else:
                #     return redirect('/slot/book/') # Redirect to home page if user is a student
                return redirect('/')
            else:
                return render(request, "login.html", {"err": True})
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(
                username, password))
            # Redirect to login page if user credentials are invalid
            return render(request, "login.html", {"invalid": True})
    else:
        return render(request, 'login.html')


# This view is used to handle logout url request and logout user
def logoutUser(request):
    logout(request)
    return redirect('/')


# This view is used to create Class slot by faculty and open slot for students
@login_required(login_url='/login/')
@permission_required('is_superuser', raise_exception=True)
def createClassSlot(request):
    if request.method == 'POST':
        class_slot_details = ClassSlotDetails()
        class_slot_details.name = request.POST.get('class_slot_name')
        class_slot_details.description = request.POST.get(
            'class_slot_description')
        class_slot_details.date = request.POST.get('class_slot_date')
        class_slot_details.start_time = request.POST.get(
            'class_slot_start_time')
        class_slot_details.end_time = request.POST.get('class_slot_end_time')
        if(request.POST.get('class_slot_link')):
            class_slot_details.link = request.POST.get('class_slot_link')
        class_slot_details.save()  # Class slot is saved in the DB
        subject = "New In-Person class Slot | " + class_slot_details.name + " | " + \
            class_slot_details.start_time + " to " + \
            class_slot_details.end_time + " | " + class_slot_details.date
        message = "Hi,\n\n" + "A new class slot has been opened for slot booking.\n\n" + "Name: " + class_slot_details.name + "\n" + "Description: " + class_slot_details.description + "\n" + "Date: " + \
            class_slot_details.date + "\n" + "Start Time: " + class_slot_details.start_time + "\n" + "End Time: " + \
            class_slot_details.end_time + "\n" + "Link: " + \
            class_slot_details.link + "\n\n" + "Regards,\n" + "गुरुSkool Team"
        all_students = User.objects.filter(is_superuser=False)
        for student in all_students:
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      [student.username], fail_silently=False)
        return redirect('/slot/')
    else:
        return render(request, 'create_class_slot.html')


# This view is used to view/return Class slot which are open to students and faculty
@login_required(login_url='/login/')
@permission_required('is_superuser', raise_exception=True)
def viewClassSlots(request):
    try:
        class_slots = ClassSlotDetails.objects.all()  # Get all class slots from DB
    except:
        class_slots = None
    # Render class slots page with all class slots
    return render(request, 'class_slots.html', {'class_slots': class_slots})


# This view is used to edit Class slot which are created by faculty
@login_required(login_url='/login/')
@permission_required('is_superuser', raise_exception=True)
def editClassSlot(request, class_slot_id):  # Get class slot id from url
    class_slot = ClassSlotDetails.objects.get(id=class_slot_id)
    if request.method == 'POST':
        class_slot.name = request.POST.get('class_slot_name')
        class_slot.description = request.POST.get('class_slot_description')
        class_slot.date = request.POST.get('class_slot_date')
        class_slot.start_time = request.POST.get('class_slot_start_time')
        class_slot.end_time = request.POST.get('class_slot_end_time')
        if(request.POST.get('class_slot_link')):
            class_slot.link = request.POST.get('class_slot_link')
        class_slot.save()  # Class slot is saved in the DB
        return redirect('/slot/')  # Redirect to home page
    else:
        # Render create class slot page with class slot details
        return render(request, 'create_class_slot.html', {'class_slot': class_slot})


# This view is used to delete Class slot which are created by faculty
@login_required(login_url='/login/')
@permission_required('is_superuser', raise_exception=True)
def deleteClassSlot(request, class_slot_id):
    class_slot = ClassSlotDetails.objects.get(
        id=class_slot_id)  # Get class slot id from url
    class_slot.delete()  # Delete class slot from DB
    return redirect('/slot/')


# This view is used to Book slots by the students based on their preferences
@login_required(login_url='/login/')
def bookClassSlot(request):
    if request.method == 'POST':
        class_slot_booking = ClassSlotBooking()
        class_slot_booking.user = request.user
        class_slot_id = request.POST.get(
            'class_slot_id')  # Get class slot id from form
        class_details = ClassSlotDetails.objects.get(
            id=class_slot_id)  # Get class slot details from DB
        class_slot_booking.class_details = class_details
        class_slot_booking.save()
        if(class_details.current_capacity > 1):  # If class slot is not full
            class_details.current_capacity = class_details.current_capacity - \
                1  # Decrease current capacity by 1
            class_details.save()
            subject = "Your Slot has been booked Successfully"
            message = "Your slot has been booked successfully. Please check your slot details in the class slot page"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                      [request.user.username])
        return render(request, 'book_success.html', {'class_details': class_details})
    else:
        try:
            class_slots = ClassSlotDetails.objects.all()
            slot_booked_by_user_list = ClassSlotBooking.objects.filter(
                user=request.user)  # Get all class slots booked by user
            slot_booked_by_user_list_id = []  # Create a list of class slot ids booked by user
            for slot in slot_booked_by_user_list:
                slot_booked_by_user_list_id.append(slot.class_details.id)
        except:
            class_slots = None  # If no class slots are available
        return render(request, 'book_slot.html', {'class_slots': class_slots, 'slot_booked_by_user_list_id': slot_booked_by_user_list_id})


# This view is used to create Group Discussion slot by faculty
@login_required(login_url='/login/')
@permission_required('is_superuser', raise_exception=True)
def createGroupDiscussion(request):
    if request.method == 'POST':
        group_discussion = GroupDiscussion()  # Create a group discussion object
        group_discussion.topic = request.POST.get('topic')
        group_discussion.number_of_groups = request.POST.get(
            'number_of_groups')
        group_discussion.date = request.POST.get('date')
        group_discussion.start_time = request.POST.get('start_time')
        group_discussion.end_time = request.POST.get('end_time')
        group_discussion.save()  # Save group discussion in DB
        for i in range(int(group_discussion.number_of_groups)):
            group_discussion_links = GroupDiscussionLinks()
            group_discussion_links.group_discussion = group_discussion
            letters = string.ascii_letters
            random_link = ''.join(random.choice(letters)
                                  for i in range(7))  # Generate random links
            group_discussion_links.link = "https://meet.jit.si/"+random_link
            group_discussion_links.save()

        return redirect('/groupdiscussion/')
    else:
        return render(request, 'create_group_discussion.html')


# This view is used to view/return Group Discussion slot which are open to students
@login_required(login_url='/login/')
def viewGroupDiscussion(request):
    try:
        # Get all group discussions from DB
        group_discussions = GroupDiscussion.objects.all()
    except:
        group_discussions = None  # If no group discussions are available
    return render(request, 'group_discussions_slot.html', {'group_discussions': group_discussions})


# This view is used to Join Group Discussion slot which are available
@login_required(login_url='/login/')
def joinGroupDiscussion(request, gd_slot_id):
    # Get group discussion from slot id
    gd_slot = GroupDiscussion.objects.get(id=gd_slot_id)
    gd_table = GroupDiscussionLinks.objects.filter(group_discussion=gd_slot).order_by(
        'link')  # Get all group discussion links from group discussion
    gd_table_links_list = []  # Create a list of group discussion links
    for gd_table_link in gd_table:
        gd_table_links_list.append(gd_table_link.link)
    timings = list(pandas.date_range(start=str(gd_slot.start_time), end=str(gd_slot.end_time), periods=int(
        gd_slot.number_of_groups)+1))  # Get all timing breakdown between start time and end time for group discussion

    return render(request, 'group_discussion.html', {'gd_slot': gd_slot, 'number_of_groups': range(gd_slot.number_of_groups), 'timings': timings, 'gd_table_links_list': gd_table_links_list})


def timeline(request):
    return render(request, "timeline.html")
