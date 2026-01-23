from django.contrib import admin
from .models import PasswordReset,Contact,Course
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TutorProfile,StudentProfile,Payment
from .models import *

admin.site.register(PasswordReset)
admin.site.register(Contact)
admin.site.register(Course)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TutorProfile)
admin.site.register(StudentProfile)
admin.site.register(Payment)
admin.site.register(Module)

admin.site.register(Resource)
# admin.site.register(Quiz)
# admin.site.register(Question)
# admin.site.register(Option)
# admin.site.register(StudentQuizAttempt)
# admin.site.register(StudentAnswer)



