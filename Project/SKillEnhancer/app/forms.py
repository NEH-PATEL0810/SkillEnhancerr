from django import forms
from .models import Contact
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, TutorProfile,StudentProfile

from django import forms
from .models import *
class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES, widget=forms.Select,required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']  
        if commit:
            user.save()
        return user

class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        fields = ['expertise', 'bio', 'profile_picture']

class StudentProfileForm(forms.ModelForm):
    area_of_interest=forms.MultipleChoiceField(
        choices=StudentProfile.INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model=StudentProfile
        fields=['college_name','degree','graduation_year','area_of_interest']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'category', 'level', 'image','description','price']


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['course', 'title','content']


class ResourceForm(forms.ModelForm):

    def __init__(self, *args, tutor=None, **kwargs):  
        super(ResourceForm, self).__init__(*args, **kwargs)
        if tutor:
            self.fields['course'].queryset = Course.objects.filter(tutor=tutor)  

    class Meta:
        model = Resource
        fields = ['course','title', 'file', 'url','video_url']

    def clean(self):
        cleaned_data = super().clean()
        # resource_type = cleaned_data.get('resource_type')
        file = cleaned_data.get('file')
        url = cleaned_data.get('url')
        video_url = cleaned_data.get('video_url') 

        if not file and not url and not video_url:
            raise forms.ValidationError("Please provide at least one resource: File, URL, or Video URL.")

        return cleaned_data  
    


# class QuizForm(forms.ModelForm):
#     class Meta:
#         model = Quiz
#         fields=['title','course']


# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model=Question
#         fields=['quiz','text']


# class OptionForm(forms.ModelForm):
#     class Meta:
#         model = Option
#         fields = ['question','text','is_correct']
        

