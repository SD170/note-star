from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Year(models.Model):
    year_choices = (
        ('1st','1st'),
        ('2nd','2nd'),
        ('3rd','3rd'),
        ('4th','4th'),
    )
    no = models.CharField(choices=year_choices, max_length = 20, null=True, blank=False)
    def __str__(self):
        if self.no == None:
            return "Year is NULL"
        return self.no

class Department(models.Model):
    name = models.CharField(max_length=50, null=True, blank =False)
    
    def __str__(self):
        if self.name == None:
            return "Dept Name is NULL"
        return self.name
    

class College (models.Model):
    name = models.CharField(max_length=100, null = True, blank=True)
    department = models.ForeignKey(Department, on_delete = models.SET_NULL, null= True, blank=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, max_length = 20, null=True, blank=False)

    def __str__(self):
        if self.name == None:
            return "College Name is NULL"
        return self.name



class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    college_name = models.ForeignKey(College,on_delete=models.SET_NULL,null =True, blank=True)

    def __str__(self):
        if self.full_name == None:
            return "Full Name is NULL"
        return self.full_name
    



class Part(models.Model):
    name = models.CharField(max_length=50, null=True, blank =True)
    def __str__(self):
        if self.name == None:
            return "Part no is NULL"
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=50, null=True, blank =False)
    
    def __str__(self):
        if self.name == None:
            return "Topic Name is NULL"
        return self.name

    

class Subject(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        if self.name == None:
            return "Subject is NULL"
        return self.name
    # def __str__(self):
    #     if self.subjectname.name == None:
    #         return "Subject is NULL"
    #     return str(self.subjectname.name)

# def user_directory_path (instance, filename):
#     return 'college_{0}/{1}'.format(instance.user.id, filename) #topiccc
# upload_to = user_directory_path, 

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_file = models.FileField(null=True, blank=True)
    
    def __str__(self):
        if self.user == None:
            return "username is NULL"
        return self.user.username

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    subject = models.ManyToManyField(Subject, max_length=50, blank=True, null=True)
    department = models.ManyToManyField(Department, max_length=50, null=True, blank=True)
    year = models.ManyToManyField(Year, max_length=10, null=True, blank=True)
    
    def __str__(self):
        if self.full_name == None:
            return "Full Name is NULL"
        return self.full_name

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True,blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    document = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank = True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    part = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, blank = True)
    created_date = models.DateTimeField(default=timezone.now())
    download = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        if self.user  == None:
            return 'Username is Null'
        return str('%s, %s, %s' % (self.user, self.subject, self.created_date))

