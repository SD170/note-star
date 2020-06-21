from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import UserForm

# from django.contrib.sessions.models import Session

from django.forms import modelformset_factory
# from ..notestar.settings import STATIC_URL,STATIC_ROOT,STATICFILES_DIRS,MEDIA_ROOT,MEDIA_URL

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media/file')
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.files import File as DjangoFile


@login_required(login_url='/login/')
def home(request):

    user = request.user
    profile = user.profile

    context = {
        'user' : user,
        'profile' : profile,
    }

    return render(request, 'details/home_page.html', context)


def register_page(request):
    user_form = UserForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():

            user = user_form.save()
            user.refresh_from_db() 

            full_name = user_form.cleaned_data.get('full_name')
            email = user_form.cleaned_data.get('email')
            c_name = request.POST.get('college_name')
            college_name, created = College.objects.get_or_create(name=c_name)  #created is always needed...otherwise...both values will be stored on college name as array...which is problem
            # print('creattttttttttttee',created,college_name)
            Profile.objects.create(user=user,full_name=full_name,email=email,college_name=college_name)
            raw_password = user_form.cleaned_data.get('password1')
            username = user.username
            checked_user = authenticate(username=username, password=raw_password)
            login(request,checked_user)

            return redirect('college_details')

    context = {
        'user_form' : user_form,
        'colleges': College.objects.all().order_by('name'),
    }

    return render(request, 'details/register_page.html', context)


def login_page(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    checked_user = authenticate(request, username=username, password = password)

    if request.user.is_authenticated:
        user=request.user
        return HttpResponse("Your'e alrady logged in")


    if checked_user is not None:
        login(request,checked_user)
        return redirect('home')
    else:
        messages.info(request,'Username or Password not correct')

    context={}
    return render(request, 'details/login_page.html', context)

@login_required(login_url='/login/')
def logout_page(request):
	logout(request)
	return redirect('login')



def college_details(request):
    user=request.user
    if request.method == 'POST':
        dept = request.POST.get('dept_name')
        dept_obj, created = Department.objects.get_or_create(name=dept)
        dept_obj.save()
        year = request.POST.get('year')
        year_obj, created = Year.objects.get_or_create(no=year)
        year_obj.save()
        college_obj = College.objects.filter(name=user.profile.college_name.name).update(department=dept_obj, year=year_obj)
        # print('ccccccccccc',college_obj)
    
    context = {
        'user' : user,
        'dept_list' : Department.objects.all().order_by('name'),
    }
    
    return render(request, 'details/college_details.html', context)

def new_note_create(request):

    if request.method == 'POST':
        user=request.user
        teacher_name = request.POST.get('teacher_name')
        subjects_name = request.POST.get('subject_name')
        topic_name = request.POST.get('topic_name')
        part_name =  request.POST.get('part_name')

        department_obj = user.profile.college_name.department
        if part_name is not None:
            part_obj , created = Part.objects.get_or_create(name=part_name)
            part_obj.save()
        else:
            part_obj=None
        # print(part_obj,)
        topic_obj, created = Topic.objects.get_or_create(name=topic_name)
        topic_obj.save()
        subject_obj, created = Subject.objects.get_or_create(name=subjects_name) 
        subject_obj.save()
        # subject_obj.ssssssssssssss
        teacher_obj, created = Teacher.objects.get_or_create(full_name=teacher_name)
        teacher_obj.save()
        teacher_obj.department.add(department_obj)
        teacher_obj.subject.add(subject_obj)
        teacher_obj.save()

        note_obj = Note.objects.create(user=user,teacher=teacher_obj,subject=subject_obj,department=department_obj,
                                        topic=topic_obj, part=part_obj)
        note_obj.save()
        

        note_id = note_obj.id
        request.session.modified = True #explanation downwards
        request.session['note_id'] = note_id  #passins values withing views with session
        # print(note_obj,note_id)
        return redirect('file_upload_form')
   
    context = {
        
    }
    return render(request, 'details/note_create.html', context)


def file_upload_form(request):
    
    return render(request, 'details/upload_file.html', {})



def file_upload(request):
    user = request.user
    note_id = request.session['note_id']    #retriving value
    # if note_id is not None:
    note_obj = Note.objects.get(id=note_id)

    request.session.pop('note_id',None) #deleting last session value
    request.session.modified = True     # changed value of next sesson wont be saved if we dont modify it...so modify explicitely

    for count, i in enumerate(request.FILES.getlist('files')):
        def process(f):
            with open(MEDIA_ROOT+ str(count), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        process(i)
        file_obj = File.objects.create(uploaded_file=i,user=user)
        file_obj.save()
        note_obj.document=file_obj
        note_obj.save()
    
    return redirect('home')

def search_note_1 (request):
    user = request.user
    department_obj = user.profile.college_name.department
    dept_teachers = department_obj.teacher_set.all()

    context = {
        'dept_teachers':dept_teachers,
    }
    
    return render(request, 'details/search_note_1.html', context)

def search_note_2 (request):
    
    user = request.user
 
    teacher_id = request.POST.get('search1')
    teacher_obj = Teacher.objects.get(id=teacher_id)
    teacher_notes = teacher_obj.note_set.all().order_by('-user')
    teacher_subjects = teacher_obj.subject.all()   #.all() holo karon eta many to many

    # single user show - no repeat
    new_teachers_notes = list()
    first_note = teacher_notes.first()
    first_note_user = first_note.user
    new_teachers_notes.append(first_note)
    for i in teacher_notes:
        if i.user != first_note_user:
            new_teachers_notes.append(i)
        first_note_user=i.user


            

    context = {
        'teacher_notes' : new_teachers_notes,
        'teacher_subjects' : teacher_subjects
    }
    
    return render(request, 'details/search_note_2.html', context)

def search_note_3(request):
    user = request.user
    subject_id = request.POST.get('search2')
    subject_obj = Subject.objects.get(id=subject_id)
    subject_notes = subject_obj.note_set.all().order_by('-user')
    # notes = Note.objects.filter(subject__id__in=subject_obj) 
    # print('nononononn',notes)
    topic_sorted_notes = subject_obj.note_set.all().order_by('-topic')
    subject_topic = list()
    for i in topic_sorted_notes:
        subject_topic.append(i.topic)
    
    try:
        new_subject_topic = list()
        first_subject_topic = subject_topic[0]
        first_topic_name = first_subject_topic.name
        new_subject_topic.append(subject_topic[0])
        for i in subject_topic:
            if i.name != first_topic_name:
                new_subject_topic.append(i)
        first_topic_name=i.name

    except:
        return HttpResponse('Internal Error SN3')
    
    
    new_subject_notes = list()
    first_note = subject_notes.first()
    first_note_user = first_note.user
    new_subject_notes.append(first_note)
    for i in subject_notes:
        if i.user != first_note_user:
            new_subject_notes.append(i)
        first_note_user=i.user




    context = {
        'subject_notes' : new_subject_notes, 
        'subjcet_topic' : new_subject_topic,
        'subject_id' : subject_id,
    }
    
    return render(request, 'details/search_note_3.html', context)


def search_note_4(request):
    user = request.user
    topic_id = request.POST.get('search3')
    subject_id = request.POST.get('subject_id')
    topic_obj = Topic.objects.get(id=topic_id)
    # topic_notes = Note.objects.filter(subject.topic.name=topic_obj.name)
    # print('sasasa',topic_id,topic_obj,topic_notes)
    # notes = Note.objects.filter(subject=topic_subject) 
    # notes = Note.objects.filter(subject__id__in=topic_obj.subject_set.all()) 
    
    sub_topic_notes = list()
    part_list=list()
    topic_notes = topic_obj.note_set.all().order_by('-user')
    for i in topic_notes:
        if int(i.subject.id) == int(subject_id):
            sub_topic_notes.append(i)
            # print(i.topic.id, topic_id)
            # if int(i.topic.id) == int(topic_id):
            #     part_list.append(i.part)

    try:
        topic_notes = topic_obj.note_set.all().order_by('topic')
        for i in topic_notes:
            if int(i.subject.id) == int(subject_id):
                if int(i.topic.id) == int(topic_id):
                        part_list.append(i.part)
            
        new_part_list = list()
        first_part = part_list[0]
        first_part_name = first_part.name
        new_part_list.append(first_part)
        for i in part_list:
            if i.name != first_part_name:
                new_part_list.append(i)
            first_part_name=i.name
    except:
        return HttpResponse('Internal Error SN4')

    
    new_topic_notes = list()
    try:
        first_note = sub_topic_notes[0]
        first_note_user = first_note.user
        new_topic_notes.append(first_note)
        for i in sub_topic_notes:
            if i.user != first_note_user:
                new_topic_notes.append(i)
            first_note_user=i.user
    except:
        return HttpResponse('No topic to search - Go back')


    context = {
        'topic_notes':new_topic_notes, 
        'part_list' : new_part_list,
        'subject_id' : subject_id,
        'topic_id' : topic_id,

    }
    
    return render(request, 'details/search_note_4.html', context)


def part_result(request):
    part_id = request.POST.get('search4')
    subject_id = request.POST.get('subject_id')
    topic_id = request.POST.get('topic_id')
    part_obj = Part.objects.get(id=part_id)
    part_notes = part_obj.note_set.all().order_by('-user')
    sub_part_notes = list()

    for i in part_notes:
        if int(i.subject.id) == int(subject_id):
            if int(i.topic.id) == int(topic_id):
                sub_part_notes.append(i)
    
    # a = File.objects.all().first()
    # print(a.uploaded_file)
    context = {
        'part_notes':sub_part_notes, 
        # 'a':a.uploaded_file,
    }
    
    return render(request, 'details/part_result.html', context)


def user_notes(request,pk):
    home_user = request.user
    away_user = User.objects.get(id=pk)
    context = dict()
    all_notes = Note.objects.all()
    all_files = File.objects.all()

    try:
        # new_teacher_notes = list()
        teacher_id = request.GET['teacher_id']
        teacher_obj = Teacher.objects.get(id=teacher_id)
        teacher_notes = teacher_obj.note_set.all()
        context['teacher_notes'] = teacher_notes
        # for i in all_notes:
        #     if i.teacher == teacher_obj:
        #         new_teacher_notes.append(i)
        # context['teacher_notes'] = new_teacher_notes
        # print(new_teacher_notes)

    except:
        teacher_id = None
        print('no_teacher_id')
        # print(context)

        pass 
    

    try:
        new_subject_notes = list()
        subject_id = request.GET['subject_id']
        subject_obj = Subject.objects.get(id=subject_id)
        subject_notes = subject_obj.note_set.all()
        for i in subject_notes:
            if i.teacher == teacher_obj:
                new_subject_notes.append(i)
        context['subject_notes'] = new_subject_notes

    except: 
        subject_id = None
        print('no_subject_id') 
        pass
    
    try: 
        new_topic_notes = list()
        topic_id = request.GET['topic_id']
        topic_obj = Topic.objects.get(id=topic_id)
        topic_notes = topic_obj.note_set.all()
        for i in topic_notes:
            if i.subject == subject_obj:
                new_topic_notes.append(i)
        context['topic_notes'] = new_topic_notes
        
    except: 
        topic_id = None
        print('no_topic_id')  
        pass    
    
    try: 
        new_part_notes = list()
        part_id = request.GET['part_id']
        part_obj = Part.objects.aget(id=part_id)
        part_notes = part_obj.note_set.all()
        for i in part_notes:
            if i.subject == subject_obj:
                new_part_notes.append(i)
        context['part_notes'] = new_part_notes
    except:
        part_id = None
        print('no_part_id')  
        pass
    
    # context = {
    #     'teacher_id' : teacher_id,
    #     'subject_id' : subject_id,
    #     'topic_id' : topic_id,
    #     'post_id' : post_id,
    # }
    
    return render(request, 'details/user_notes.html', context)


