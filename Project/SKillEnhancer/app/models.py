from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.conf import settings

# User = get_user_model() 
class PasswordReset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"



class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=254)
    phone=models.IntegerField()
    message=models.TextField()
    def __str__(self):
        return self.name
    





# User = get_user_model()
class CustomUser(AbstractUser):
    USER_TYPES=[
         ('student', 'Student'),
        ('tutor', 'Tutor'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    def is_tutor(self):
        return self.user_type == 'tutor'

    def is_student(self):
        return self.user_type == 'student'
    
    
    
class TutorProfile(models.Model):
        EXPERTISE_CHOICES = [
        ('web_development', 'Web Development'),
        ('app_development', 'App Development'),
        ('ai_ml', 'AI / Machine Learning'),
        ('data_science', 'Data Science'),
        ('cloud_computing', 'Cloud Computing'),
        ('cybersecurity', 'Cybersecurity'),
    ]
        user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='tutor_profile')
        expertise = models.CharField(max_length=255)  # Subject expertise
        bio = models.TextField(blank=True, null=True)
        profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True,default='profile_pics/default.png')

        def __str__(self):
            return self.user.username

class Course(models.Model):
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="courses", null=True, blank=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    level = models.CharField(max_length=50, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Beginner')
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    description = models.TextField(null=True)  # Course Overview
    price = models.IntegerField()
    # created_at = models.DateTimeField(auto_now_add=True, default=now)

    def __str__(self):
        return self.title


class StudentProfile(models.Model):
    INTEREST_CHOICES=[
        ('programming','Programming'),
        ('machine_learning','Machine Learning'),
        ('networking','Networking'),
        ('data_science','Data Science'),
        ('app_development','App Development'),
        ('cybersecurity','Cybersecurity'),

    ]
    YEAR=[
        ('2025','2025'),
        ('2026','2026'),
        ('2027','2027'),
        ('2028','2028'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    college_name = models.CharField(max_length=255, blank=True, null=True)
    degree = models.CharField(max_length=255, blank=True, null=True)
    graduation_year = models.CharField(max_length=255,null=True)
    area_of_interest = models.CharField(max_length=255, choices=INTEREST_CHOICES, blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    enrolled_courses = models.ManyToManyField(Course,blank=True)
    def __str__(self):
        return self.user.username
    


class Payment(models.Model):
  user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
  order_id=models.CharField(max_length=100,unique=True)
  payment_id=models.CharField(max_length=100,blank=True,null=True)
  amount=models.IntegerField()
  course=models.ForeignKey(Course,on_delete=models.CASCADE,blank=True,null=True)
  is_paid=models.BooleanField(default=False)

  def __str__(self):
      return self.order_id
  



class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Resource(models.Model):
    RESOURCE_TYPES = [('PDF', 'PDF'), ('Video', 'Video'), ('URL', 'URL')]
    
    # module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="resources")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="resources",null=True,blank=True)
    title = models.CharField(max_length=200)
    # resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to='resources/', blank=True, null=True, 
                            help_text="Upload a PDF or Video file")
    url = models.URLField(blank=True, null=True, help_text="Provide a website link if applicable")
    video_url = models.URLField(blank=True, null=True, 
                                help_text="Provide a YouTube or Video link for video resources")
   
    def __str__(self):
        return f"{self.course.title} - {self.title}"

# class Quiz(models.Model):
#     course=models.ForeignKey(Course,on_delete=models.CASCADE)
#     title=models.CharField(max_length=200)

# class Question(models.Model):
#     quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE, related_name="questions")
#     text=models.TextField()

# class Option(models.Model):
#     question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name="options")
#     text=models.CharField(max_length=255)
#     is_correct = models.BooleanField(default=False)

# class StudentQuizAttempt(models.Model):
#     student=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
#     score=models.IntegerField(default=0)

# class StudentAnswer(models.Model):
#     attempt=models.ForeignKey(StudentQuizAttempt,on_delete=models.CASCADE)
#     question=models.ForeignKey(Question,on_delete=models.CASCADE)
#     selected_option=models.ForeignKey(Option,on_delete=models.CASCADE,null=True,blank=True)
#     is_correct=models.BooleanField(default=False)
