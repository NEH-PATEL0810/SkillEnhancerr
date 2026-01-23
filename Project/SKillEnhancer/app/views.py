from django.shortcuts import render
from django.shortcuts import redirect,render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from django.http import HttpResponse
from .forms import ContactForm
from django.core.mail import send_mail,EmailMessage
from django.core.paginator import Paginator
from django.db.models import Q
from .filters import CourseFilter
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import *
import logging
from django.http import JsonResponse
import razorpay
from django.http import HttpResponseForbidden
import json

User = get_user_model()
# Create your views here.
def Home(request):
    return render(request, 'base.html')


def contact(request):
      if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            message = form.cleaned_data["message"]
            Contact= form.save()

            # Send email to user
            send_mail(
                subject=f"Thank you for contacting us, {name}!",
                message=f"Hello {name},\n\nWe have received your message:\n\n{message}\n\nYour phone number: {phone}\n\nWe will get back to you soon.",
                from_email="your_email@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )
            return render(request, "contact_success.html", {"name": name})
      else:
        form = ContactForm()

      return render(request, "contact.html", {"form": form})


    

            
# @login_required
def Interface(request):
    return render(request, 'index.html')

# @login_required
def Explore_Course(request):
    
    courses = Course.objects.all()

    # Get filter values from request
    title = request.GET.get('title')
    selected_categories = request.GET.getlist('category')
    selected_levels = request.GET.getlist('level')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    rating = request.GET.get('rating')

    # Apply filters
    if title:
        courses = courses.filter(title__icontains=title)
    
    if selected_categories:
        courses = courses.filter(category__in=selected_categories)

    if selected_levels:
        courses = courses.filter(level__in=selected_levels)

    if min_price:
        courses = courses.filter(price__gte=min_price)

    if max_price:
        courses = courses.filter(price__lte=max_price)

    if rating:
        courses = courses.filter(rating__gte=rating)
    
    paginator = Paginator(courses, 10)  # Show 10 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    context = {
        # 'courses': courses,
        'categories': ['web-development', 'app-development', 'ai-ml', 'cloud-computing'],
        'levels': ['Beginner', 'Intermediate', 'Advanced'],
        'selected_categories': selected_categories,  
        'selected_levels': selected_levels,
         'courses': page_obj,  # Paginated courses
        'paginator': paginator,
        'page_obj': page_obj,
    }
   
    return render(request, 'Explore_courses.html',context)
    # return render(request,'Explore_courses.html')


@login_required
def student_explore_course(request):
    courses = Course.objects.all()

    # Get filter values from request
    title = request.GET.get('title')
    selected_categories = request.GET.getlist('category')
    selected_levels = request.GET.getlist('level')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    rating = request.GET.get('rating')

    # Apply filters
    if title:
        courses = courses.filter(title__icontains=title)
    
    if selected_categories:
        courses = courses.filter(category__in=selected_categories)

    if selected_levels:
        courses = courses.filter(level__in=selected_levels)

    if min_price:
        courses = courses.filter(price__gte=min_price)

    if max_price:
        courses = courses.filter(price__lte=max_price)

    if rating:
        courses = courses.filter(rating__gte=rating)
    
    paginator = Paginator(courses, 10)  # Show 10 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # is_premium = False
    student_profile = None
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        student_profile = request.user.student_profile

    context = {
        # 'courses': courses,
        'categories': ['web-development', 'app-development', 'ai-ml', 'cloud-computing'],
        'levels': ['Beginner', 'Intermediate', 'Advanced'],
        'selected_categories': selected_categories,  
        'selected_levels': selected_levels,
         'courses': page_obj,  # Paginated courses
        'paginator': paginator,
        'page_obj': page_obj,
        'student_profile': student_profile,
        # 'is_premium': is_premium,

    }
   
    # return render(request, 'Explore_courses.html',context)
    return render(request,'student_explore_course.html',context)
    
def StudentRegisterView(request):
    if request.method == "POST":
       user_form=CustomUserCreationForm(request.POST)
       student_form=StudentProfileForm(request.POST)

       if user_form.is_valid():
           user = user_form.save(commit=False)
           user_type = user_form.cleaned_data.get("user_type")

           user.save()

           if user_type=='student':
            if student_form.is_valid():
                student_profile=student_form.save(commit=False)
                student_profile.user=user
                student_profile.area_of_interest = ",".join(student_form.cleaned_data['area_of_interest'])  
                student_profile.save()

            else:
               messages.error(request,"Student profile details are invalid")
               return render(request,'student_register.html',{'user_form':user_form,'student_form':student_form})
           login(request,user)
           return redirect('student_dashboard' if user_type=='student' else 'home') 
    else:
         user_form = CustomUserCreationForm()
         student_form = StudentProfileForm()
    
    return render(request, 'student_register.html', {'user_form': user_form, 'student_form': student_form})
          
def TutorRegisterView(request):
     if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        tutor_form = TutorProfileForm(request.POST, request.FILES)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user_type = user_form.cleaned_data.get("user_type")

            user.save() 
                      
            if user_type == 'tutor':  
                if tutor_form.is_valid():
                     
                    tutor_profile = tutor_form.save(commit=False)
                    tutor_profile.user = user
                    tutor_profile.save()

                else:
                    messages.error(request,"Tutor profile details are invalid")
                    return render(request, 'tutor_register.html', {'user_form': user_form, 'tutor_form': tutor_form})
            login(request, user)
            return redirect('tutor_dashboard' if user_type == 'tutor' else 'student_dashboard')  
        else:
            messages.error(request,"User registration failed.Please check the form")
            return render(request,'tutor_register.html',{'user_form' : user_form,'tutor_form':tutor_form})
     else:
        user_form = CustomUserCreationForm()
        tutor_form = TutorProfileForm()

     return render(request, 'tutor_register.html', {'user_form': user_form, 'tutor_form': tutor_form})



def student_login(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]

        user = authenticate(request,username=username,password=password)

        if user and StudentProfile.objects.filter(user=user).exists():
            login(request,user)
            return redirect('student_dashboard')
        else:
            messages.error(request,"Invalid credentials or student profile not found.")
    return render(request,'student_login.html')

def tutor_login(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user and TutorProfile.objects.filter(user=user).exists():
            login(request, user)
            return redirect("tutor_dashboard")  # Redirect to tutor dashboard
        else:
            messages.error(request, "Invalid credentials or tutor profile not found.")

    return render(request, "tutor_login.html")

def LogoutView(request):
    logout(request)
    print("You have been Logged out")
    return redirect('home')

def ForgotPasswordTutor(request):
    # if request.method == "POST":
    #     email=request.POST.get('email')

    #     try:
    #         user = User.objects.get(email=email,user_type='Tutor')
    #         new_password_reset = PasswordReset.objects.create(user=user)
    #         new_password_reset.save()

    #         password_reset_url = reverse('reset-password-tutor', kwargs={'reset_id': new_password_reset.reset_id})
    #         full_password_reset_url = f"{request.scheme}://{request.get_host()}{password_reset_url}"
    #         # email_body = f"Heyy I am Neh Patel,Reset your password using the link below:\n\n\n{full_password_reset_url}"
    #         print(full_password_reset_url)  # Debugging output

    #         email_body = f"Reset your password using the link below:\n\n\n{full_password_reset_url}"
   
    #         email_message = EmailMessage(
    #         subject='Reset your password', # email subject
    #         body=email_body,
    #         from_email=settings.EMAIL_HOST_USER, # email sender
    #         to=[email] # email  receiver 
    #     )
                 
    #         email_message.send(fail_silently=True)

    #         return redirect('password-reset-sent-tutor',reset_id=new_password_reset.reset_id)

    #     except User.DoesNotExist:
    #         messages.error(request,f"No user with email '{email}' found")
    #         return redirect('forgot-password-tutor')

    # return render(request, 'tutor_forgot_password.html')
    
    if request.method == "POST":
        email=request.POST.get('email')

        try:
            user = CustomUser.objects.get(email=email,user_type='tutor')
            new_password_reset = PasswordReset.objects.create(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password-tutor', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f"{request.scheme}://{request.get_host()}{password_reset_url}"
            # email_body = f"Heyy I am Neh Patel,Reset your password using the link below:\n\n\n{full_password_reset_url}"
            print(full_password_reset_url)  # Debugging output

            email_body = f"Reset your password using the link below:\n\n\n{full_password_reset_url}"
   
            email_message = EmailMessage(
            subject='Reset your password', # email subject
            body=email_body,
            from_email=settings.EMAIL_HOST_USER, # email sender
            to=[email] # email  receiver 
        )
                 
            email_message.send(fail_silently=True)

            return redirect('password-reset-sent-tutor',reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request,f"No user with email '{email}' found")
            return redirect('forgot-password-tutor')

    return render(request, 'tutor_forgot_password.html')


def PasswordResetSenttutor(request, reset_id):
    context = {'reset_id': reset_id}
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
     return render(request, 'password_reset_sent_tutor.html', context)

    else:
        messages.error(request,'Invalid reset Id')
        return redirect('forgot-password-tutor')

def ResetPasswordTutor(request, reset_id):
    # def ResetPassword(request, reset_id):
    try:
        password_reset_entry = PasswordReset.objects.get(reset_id=reset_id)
    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset ID')
        return redirect('forgot-password-tutor')
    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        password_have_error=False

        if password != confirm_password:
            password_have_error=True
            messages.error(request, 'Passwords do not match')
            # return redirect('reset-password', reset_id=reset_id)

      
        # if not password or len(password) < 5:
        #     password_have_error=True
        #     messages.error(request, 'Password must be at least 5 characters long')
        #     # return redirect('reset-password', reset_id=reset_id)
        
        if password_have_error:  # Stop execution if there was an error
            return redirect('reset-password-tutor', reset_id=reset_id)
        
        expiration_time = password_reset_entry.created_when + timezone.timedelta(minutes=10)
        if timezone.now() > expiration_time:
            messages.error(request, 'Reset link has expired')
            password_reset_entry.delete()
            return redirect('forgot-password-tutor')

        user = password_reset_entry.user
        user.set_password(password)
        user.save()

        password_reset_entry.delete()

        logout(request)
        
        messages.success(request, 'Password reset successfully. You can now login.')
        return redirect('tutor_login')

    return render(request, 'reset_password_tutor.html')


def ForgotPasswordStudent(request):
    if request.method=="POST":
       email = request.POST.get('email')

       try:
            user = CustomUser.objects.get(email=email,user_type='student')  # Ensure it's a student
            new_password_reset = PasswordReset.objects.create(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password-student', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f"{request.scheme}://{request.get_host()}{password_reset_url}"

            print(full_password_reset_url)

            email_body = f"Reset your password using the link below:\n\n{full_password_reset_url}"
            email_message = EmailMessage(
                subject='Student: Reset your password',
                body=email_body,
                from_email=settings.EMAIL_HOST_USER,
                to=[email]
            )

            email_message.send(fail_silently=True)

            return redirect('password-reset-sent-student', reset_id=new_password_reset.reset_id)

       except User.DoesNotExist:
            messages.error(request, f"No student with email '{email}' found")
            return redirect('forgot-password-student')

    return render(request, 'student_forgot_password.html')


def PasswordResetSentStudent(request, reset_id):
    context = {'reset_id': reset_id}
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent_student.html',context)
    else:
        messages.error(request, 'Invalid reset Id')
        return redirect('forgot-password-student')


def ResetPasswordStudent(request, reset_id):
    try:
        password_reset_entry = PasswordReset.objects.get(reset_id=reset_id)
    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset ID')
        return redirect('forgot-password-student')

    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        password_have_error=False

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('reset-password-student', reset_id=reset_id)
        
        if password_have_error:  # Stop execution if there was an error
            return redirect('reset-password-tutor', reset_id=reset_id)


        expiration_time = password_reset_entry.created_when + timezone.timedelta(minutes=10)
        if timezone.now() > expiration_time:
            messages.error(request, 'Reset link has expired')
            password_reset_entry.delete()
            return redirect('forgot-password-student')

        user = password_reset_entry.user
        user.set_password(password)
        user.save()

        password_reset_entry.delete()

        logout(request)

        messages.success(request, 'Password reset successfully. You can now log in.')
        return redirect('student_login')

    return render(request, 'reset_password_student.html')

# @login_required
def Premium_Plan(request):
    return render(request,'premium_plan.html')

def student_premium_Plan(request):
    student_profile = None
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        student_profile = request.user.student_profile
    return render(request,'student_premium_plan.html', {'student_profile': student_profile})

@login_required
def tutor_dashboard(request):
    tutor = request.user  # Get the logged-in tutor
    courses = Course.objects.filter(tutor=tutor) 
    return render(request, 'tutor_dashboard.html',{'courses':courses})
@login_required
def student_dashboard(request):
    # if not request.user.is_student():
        # return redirect('home')  # Redirect non-tutors to home
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
        enrolled_courses = student_profile.enrolled_courses.all()  # Ensure courses are fetched
    except StudentProfile.DoesNotExist:
        student_profile = None
        enrolled_courses = []  # Avoid errors if no profile exists

    context = {
        'student_profile': student_profile,
        'enrolled_courses': enrolled_courses,
    }
    return render(request, 'student_dashboard.html', context)

# Premium User-Only Content
# @login_required
# def premium_content(request):
#     if not request.user.is_premium():
#         return redirect('subscription_page')  # Redirect non-premium users
#     return render(request, 'premium_content.html')


# client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

# @login_required
# def create_payment(request):
#     if request.user.is_authenticated and hasattr(request.user,'studentprofile'):
#         amount=100
#         currency="INR"
#         payment_order = client.order.create({
#             "amount":amount,
#             "currency":currency,
#             "payment_capture":"1"
#         })

#         Payment.objects.create(user=request.user,order_id=payment_order["id"],amount=amount/100)

#         return JsonResponse(payment_order)
#     else:
#         return JsonResponse({"error": " Only students can upgrade to premium."},status=403)
    

# @login_required
# def payment_success(request):
#     if request.method=="POST":
#         order_id=request.POST.get("order_id")
#         payment_id=request.POST.get("payment_id")

#         payment=Payment.objects.get(order_id=order_id)
#         payment.payment_id=payment_id
#         payment.status="Paid"
#         payment.save()

#         student=StudentProfile.objects.get(user=request.user)
#         student.is_premium=True
#         student.save()

#         send_mail(
#             "Premium Plan Activated!",
#             "Congrats!! Your SkillEnhancer Premium pan has been activated",
#             [request.user.email],
#             fail_silently=False,
#         )

#         return JsonResponse({"message":"Payment succesful and Premium Activated!"})

#     return JsonResponse({"error" : "Invalid Request"},status=400)


from django.views.decorators.csrf import csrf_exempt
import logging
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)
@login_required
def initiate_payment(request):
    if request.method=="POST":
        try:
           amount=int(request.POST.get("amount"))*100

           client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
           order_data = {
            "amount":amount,
            "currency":"INR",
            "payment_capture":"1",
             }
        
           order = client.order.create(data=order_data)
           logger.info(f"Order created: {order}")
           
           payment=Payment.objects.create(order_id=order["id"],amount=amount)
           payment.save()

           return JsonResponse(order)

        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return JsonResponse({"success": False, "error": str(e)})
    
    return render(request,"payment.html")


@csrf_exempt
def verify_payment(request):
    if request.method=="POST":
        payment_id = request.POST.get("payment_id")
        order_id = request.POST.get("order_id")

        try:
            payment = Payment.objects.get(order_id=order_id)
            payment.payment_id=payment_id
            payment.is_paid = True
            payment.save()

            student_profile = get_object_or_404(StudentProfile, user=request.user)
            student_profile.is_premium = True
            student_profile.save()
            return JsonResponse({"success":True})
        
        except  Payment.DoesNotExist:
            return JsonResponse({"success":False,"error":"Order not found"})
    
    return JsonResponse({"success":False,"error":"Invalid request"})
     

def payment_success_page(request):
    return render(request,"payment_success.html")                

def premium_feature(request):
    if not request.user.is_authenticated or not request.user.studentprofile.is_premium:
        return HttpResponseForbidden("This feature is for premium users only.")
    return render(request,'student_dashboard.html')

def payment(request):
    return render(request,'payment.html')


@login_required
def add_course(request):
    form = CourseForm()
    course = Course.objects.all() 
    courses = Course.objects.filter(tutor=request.user)  
    last_course = courses.last()
    if request.method=="POST":
        form=CourseForm(request.POST,request.FILES)
        if form.is_valid():
            course=form.save(commit=False)
            course.tutor=request.user
            course.save()
            messages.success(request, "Course added successfully!")
            return redirect('add_module',course.id)
        # else:
        #     form=CourseForm()
    return render(request,'add_course.html',{'form':form,'courses': courses,'course':course})


@login_required
def add_module(request,course_id):
    form=ModuleForm()
    # courses = Course.objects.all()
    courses = Course.objects.filter(tutor=request.user) 
    course=get_object_or_404(Course,id=course_id)
    if request.method == "POST":
        form=ModuleForm(request.POST,request.FILES)
        if form.is_valid():
            module=form.save(commit=False)
            module.course=course
            module.save()
            return redirect('add_module', course_id=course.id)
        # else:
    return render(request,'add_module.html',{'form':form,'course':course,'courses':courses})

@login_required
def add_resource(request,course_id):
    form=ResourceForm()
    # courses = Course.objects.all()
    courses = Course.objects.filter(tutor=request.user) 
    # modules = Module.objects.all()  
    # module=get_object_or_404(Module,id=module_id)
    course=get_object_or_404(Course,id=course_id,tutor=request.user)
    form = ResourceForm()
    if request.method == "POST":
        form = ResourceForm(request.POST,request.FILES,tutor=request.user)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.course=course
            resource.save()
            messages.success(request,"Resource added successfully!")
            return redirect('tutor_dashboard')
    else:
        form = ResourceForm(tutor=request.user)
    # else:
    #     form=ResourceForm()
    return render(request,'add_resource.html',{'form':form,'course':course, 'courses': courses})
        


# @login_required
# def add_quiz(request):
#     form=QuizForm()
#     if request.method == "POST":
#         form=QuizForm(request.POST)

#         if form.is_valid():
#             form.save()
#             messages.success("Quiz has been addded successfully")
#             return redirect('tutor_dashboard')
#     return render(request,'add_quiz.html',{'form':form})


# @login_required
# def add_question(request,quiz_id):
#     quiz=get_object_or_404(Quiz,id=quiz_id)
#     form=QuestionForm(initial={'quiz':quiz})
#     if request.method == "POST":
#         form = QuestionForm(request.POST)

#         if form.is_valid():
#             form.save()
#             messages.successs("Question added")
#             return redirect('add_question',quiz_id=quiz.id)
#     return render(request,'add_question.html',{'form':form,'quiz':quiz})


# @login_required
# def add_option(request, question_id):
#     question = get_object_or_404(Question, id=question_id)
#     form = OptionForm(initial={'question': question})
#     if request.method == "POST":
#         form = OptionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('add_option', question_id=question.id)
#     return render(request, 'add_option.html', {'form': form, 'question': question})

# @login_required
# def manage_quiz(request):
#     quiz_form = QuizForm()
#     question_form=QuestionForm()
#     option_form=OptionForm()
#     quizzes=Quiz.objects.all()

#     if request.method == "POST":
#         if "create_quiz" in request.POST:
#             quiz_form=QuizForm(request.POST)
#             if quiz_form.is_valid():
#                 quiz_form.save()
#                 messages.success(request,"Quiz has been added")
#                 return redirect('manage_quiz')
        
#         elif "add_question" in request.POST:
#             question_form = QuestionForm(request.POST)
#             quiz_id = request.POST.get('quiz')
#             if quiz_id:
#                 quiz=Quiz.objects.get(id=quiz_id)
#                 if Question.objects.filter(quiz=quiz).count()>=10:
#                     messages.error(request,"A quiz can have only up to 10 questions.")
                
#                 elif question_form.is_valid():
#                      question_form.save()
#                      messages.success(request,"Question has been added")
#             return redirect('manage_quiz')
        
#         elif "add_option" in request.POST:
#             option_form=OptionForm(request.POST)
#             if option_form.is_valid():
#                 option=option_form.save(commit=False)
#                 if option.is_correct:
#                     Option.objects.filter(question=option.question,is_correct=True).update(is_correct=False)
                
#                 option.save()
#                 return redirect('manage_quiz')
            
    
#     return render(request,'manage_quiz.html',{
#         'quiz_form':quiz_form,
#         'question_form':question_form,
#         'option_form':option_form,
#         'quizzes':quizzes
#     })



# @login_required
# def get_questions(request,quiz_id):
#     questions=Question.objects.filter(quiz_id=quiz_id).values('id','text')
#     return JsonResponse({'questions': list(questions)})

# @login_required
# def start_quiz(request,quiz_id):
#     quiz = get_object_or_404(Quiz,id=quiz_id)
#     questions = Question.objects.filter(quiz=quiz)
#     return render(request,'start_quiz.html',{'quiz':quiz,'questions':questions})
# @login_required
# def submit_quiz(request,quiz_id):
#     if request.method=="POST":
#         quiz = get_object_or_404(Quiz,id=quiz_id)
#         attempt = StudentQuizAttempt.objects.create(student=request.CustomUser,quiz=quiz,score=0)

#         total_score = 0
#         for question in quiz.question_set.all():
#             selected_option_id = request.POST.get(f'question_{question.id}')
#             if selected_option_id:
#                 selected_option = Option.objects.get(id=selected_option_id)
#                 is_correct=selected_option.is_correct
#                 StudentAnswer.objects.create(attempt=attempt,question=question,selected_option=selected_option,is_correct=is_correct)
#                 if is_correct:
#                     total_score += 1
#         attempt.score=total_score
#         attempt.save()

#         return redirect('quiz_analysis',attempt.id)
    
# @login_required
# def quiz_analysis(request,attempt_id):
#     attempt = get_object_or_404(StudentQuizAttempt,id=attempt_id)
#     answers=StudentAnswer.objects.filter(attempt=attempt)

#     return render(request,'quiz_analysis.html',{'attempt':attempt,'answers':answers})


            

@login_required
def tutor_your_courses(request):
        tutor = request.user 
        courses = Course.objects.filter(tutor=tutor)  
    
    # Search functionality
        query = request.GET.get("q")
        if query:
         courses = courses.filter(title__icontains=query)


        return render(request,'tutor_your_courses.html',{'courses':courses})
@login_required
def update_course_page(request):
        tutor = request.user  # Get the logged-in tutor
        courses = Course.objects.filter(tutor=tutor)  # Show only tutor's courses
    
    # Search functionality
        query = request.GET.get("q")
        if query:
         courses = courses.filter(title__icontains=query)


        return render(request,'update_course_page.html',{'courses':courses})
@login_required
def delete_course_page(request):
        tutor = request.user  # Get the logged-in tutor
        courses = Course.objects.filter(tutor=tutor)  # Show only tutor's courses
    
    # Search functionality
        query = request.GET.get("q")
        if query:
         courses = courses.filter(title__icontains=query)


        return render(request,'delete_course_page.html',{'courses':courses})

@login_required
def tutor_base(request):
    return render(request,'tutor_base.html')
@login_required
def student_base(request):
    return render(request,'student_base.html')


@login_required
def edit_course(request,course_id):
    course = get_object_or_404(Course,id=course_id,tutor=request.user)
    form=CourseForm(instance=course)
    if request.method == "POST":
        form =CourseForm(request.POST,request.FILES,instance=course)
        if form.is_valid():
            form.save()
            messages.success(request,"Course updated successfully!")
            return redirect('tutor_your_courses')
        
        # else:
        
    return render(request,"edit_course.html",{"form":form,"course":course})

@login_required
def delete_course(request,course_id):
    course = get_object_or_404(Course,id=course_id,tutor=request.user)
    if request.method == "POST":
        course.delete()
        messages.success(request,"Courses deleted successfully!")
        return redirect('tutor_your_courses')
    return render(request,"delete_course.html",{"course":course})


@login_required
def edit_module(request,module_id):
    module = get_object_or_404(Module,id=module_id,course__tutor=request.user)
    form =ModuleForm(instance=module)
    
    if request.method == "POST":
        form = ModuleForm(request.POST,instance=module)
        if form.is_valid():
            form.save()
            messages.success(request,"Module updated successfully!")
            return redirect('edit_module',module_id=module.id)
    
    return render(request,"edit_module.html",{"form":form,"module":module})

@login_required
def edit_resource(request,resource_id):
    resource= get_object_or_404(Resource,id=resource_id,course__tutor=request.user)
    form = ResourceForm(instance=resource)
    if request.method=="POST":
        form = ResourceForm(request.POST,request.FILES,instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request,"Resource updated successfully!")
            return redirect('edit_resource',resource_id=resource    .id)
    return render(request,"edit_resource.html",{"form":form,"resource":resource})

@login_required
def course_detail(request,course_id):
    course=get_object_or_404(Course,id=course_id)
    modules=Module.objects.filter(course=course)
    resources=Resource.objects.filter(course=course)
    # quizzes=Quiz.objects.filter(course=course)

    return render(request,"course_detail.html",{
        "course":course,
        "modules":modules,
        "resources":resources,
        # "quizzes":quizzes
    })



# @login_required
# def edit_quiz(request,quiz_id):
#     quiz=get_object_or_404(Quiz,id=quiz_id,course__tutor=request.user)
#     form = QuizForm(instance=quiz)

#     if request.method == "POST":
#         form=QuizForm(request.POST,instance=quiz)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Quiz updated successfully!")
#             return redirect("course_detail",course_id=quiz.course.id)
    
#     return render(request,"edit_quiz.html",{"form":form,"quiz":quiz})


# @login_required
# def edit_question(request,question_id):
#     question=get_object_or_404(Question,id=question_id,quiz__course__tutor=request.user)
#     form = QuestionForm(instance=question)

#     if request.method == "POST":
#         form=QuestionForm(request.POST,instance=question)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Question updated successfully")
#             return redirect('edit_quiz',quiz_id=question.quiz_id)
    
#     return render(request,"edit_question.html",{"form":form,"question":question})


# @login_required
# def edit_option(request,option_id):
#     option = get_object_or_404(Option,id=option_id,question__quiz__course__tutor=request.user)
#     form = OptionForm(instance=option)

#     if request.method == "POST":
#         form = OptionForm(request.POST,instance=option)
#         if form.is_valid():
#             form.save()
#             messages.success(request,"Option Updated successfully!")
#             return redirect('edit_question',question_id=option.question.id)

#     # else:
#     #     form = OptionForm(insatnce=option)

#     return render(request,"edit_option.html",{"form":form,"option":option})
 

@login_required
def course_initiate_payment(request):
    if request.method=="POST":
        try:
            data = json.loads(request.body)
            amount=int(data["amount"])*100
            course_id=data["course_id"]

            client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
            order_data = {
                "amount":amount,
                "currency":"INR",
                "payment_capture":"1",
            }

            order = client.order.create(data=order_data)

            payment = Payment.objects.create(order_id=order["id"],amount=amount,user=request.user,course_id=course_id)
            payment.save()

            return JsonResponse(order)
        except Exception as e:
            return JsonResponse({"success":False,"error":str(e)})
        
    return JsonResponse({"success":False,"error":"Invalid request"})

@csrf_exempt
def course_verify_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        payment_id = data.get("payment_id")
        order_id=data.get("order_id")
        course_id=data.get("course_id")

        try:
            payment = Payment.objects.get(order_id=order_id)
            payment.payment_id = payment_id
            payment.is_paid = True
            payment.save()

            student_profile = get_object_or_404(StudentProfile,user=request.user)
            course = get_object_or_404(Course,id=course_id)

            student_profile.enrolled_courses.add(course)
            student_profile.save()

            return JsonResponse({"success":True})
        
        except Payment.DoesNotExist:
            return JsonResponse({"success":False,"error":"Order not found"})
    
    return JsonResponse({"success":False,"error":"Invalid request"})


@login_required
def student_course_detail(request,course_id):
    course=get_object_or_404(Course,id=course_id)
    modules=course.modules.all()
    resources=course.resources.all()
    # quizzes=Quiz.objects.filter(course=course)

    student_profile=None
    is_premium = False
    is_enrolled = False

    if request.user.is_authenticated:
        student_profile=StudentProfile.objects.filter(user=request.user).first()
        if student_profile:
            is_premium = student_profile.is_premium
            is_enrolled=course in student_profile.enrolled_courses.all()

    context = {
        'course':course,
        'modules':modules,
        'resources':resources,
        # 'quizzes':quizzes,
        'is_premium':is_premium,
        'is_enrolled':is_enrolled
                }

    return render(request,'student_course_detail.html',context)


# @login_required
# def quiz_detail(request,quiz_id):
#     quiz = get_object_or_404(Quiz,id=quiz_id)
#     return render(request,'quiz_detail.html',{'quiz':quiz})

