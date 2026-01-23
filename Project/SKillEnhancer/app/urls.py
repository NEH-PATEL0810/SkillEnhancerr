from django.urls import path
from .import views
import uuid
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Home, name='home'),
    path('interface/', views.Interface, name='interface'),
    path('register/', views.StudentRegisterView, name='student_register'),
    path('tutor_register/', views.TutorRegisterView, name='tutor_register'),
     path('tutor_dashboard/', views.tutor_dashboard, name='tutor_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('Student_login/', views.student_login, name='student_login'),
    path('tutor_login/', views.tutor_login, name='tutor_login'),
    path('contact/', views.contact, name='contact'),
    path('Explore_Course/', views.Explore_Course, name='explorecourse'),
    path('Student_Explore_Course/', views.student_explore_course, name='student_explore_course'),
    path('Premium_plan/', views.Premium_Plan, name='Premium_Plan'),
    path('logout/', views.LogoutView, name='logout'),
    path('forgot-password/tutor/', views.ForgotPasswordTutor, name='forgot-password-tutor'),
    path('password-reset-sent/tutor/<uuid:reset_id>/', views.PasswordResetSenttutor, name='password-reset-sent-tutor'),
    path('reset-password/tutor/<uuid:reset_id>/', views.ResetPasswordTutor, name='reset-password-tutor'),
    path('forgot-password/student/', views.ForgotPasswordStudent, name='forgot-password-student'),
    path('password-reset-sent/student/<uuid:reset_id>/', views.PasswordResetSentStudent, name='password-reset-sent-student'),
    path('reset-password/student/<uuid:reset_id>/', views.ResetPasswordStudent, name='reset-password-student'),
    path("initiate-payment/", views.initiate_payment, name="initiate_payment"),
    path("verify-payment/", views.verify_payment, name="verify_payment"),
    path("payment-success/", views.payment_success_page, name="success_page"),
    path("premium-feature/", views.premium_feature, name="premium-feature"),
    path("payment/", views.payment, name="payment"),
    path("add-course/", views.add_course, name="add_course"),
    path("add-module/<int:course_id>", views.add_module, name="add_module"),
    path("add-resource/<int:course_id>", views.add_resource, name="add_resource"),
    # path("manage-quiz/", views.manage_quiz, name="manage_quiz"),
    path("your_courses", views.tutor_your_courses, name="tutor_your_courses"),
    path("update_course/", views.update_course_page, name="update_course"),
    path("delete_course/", views.delete_course_page, name="delete_course"),
    path("home/", views.tutor_base, name="tutor_base"),
    path("Student-home/", views.student_base, name="student_base"),
    path("student-premium-plan/", views.student_premium_Plan, name="student_premium_plan"),
    # path("start-quiz/<int:quiz_id>/", views.start_quiz, name="start_quiz"),
    # path('get-questions/<int:quiz_id>/',views.get_questions,name="get_questions"),
    # path('quiz/<int:quiz_id>/submit/',views.submit_quiz,name="submit_quiz"),
    # path('quiz/<int:quiz_id>/',views.start_quiz,name="start_quiz"),
    # path('quiz/analysis/<int:attempt_id>/',views.quiz_analysis,name="quiz_analysis"),
     path('course/edit/<int:course_id>/', views.edit_course, name='edit_course'),
     path('course/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('module/edit/<int:module_id>/', views.edit_module, name='edit_module'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('resource/edit/<int:resource_id>/', views.edit_resource, name='edit_resource'),
    # path('quiz/edit/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    # path('question/edit/<int:question_id>/', views.edit_question, name='edit_question'),
    # path('option/edit/<int:option_id>/', views.edit_option, name='edit_option'),
     path("course_initiate_payment/", views.course_initiate_payment, name="course_initiate_payment"),
    path("course_verify_payment/", views.course_verify_payment, name="course_verify_payment"),
    path('student_course/<int:course_id>/',views.student_course_detail,name='student_course_detail'),
    # path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),







  


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)