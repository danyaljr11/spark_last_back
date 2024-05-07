from django.contrib import admin
from .models import *


# Register your models here.


admin.site.register(Member)
admin.site.register(Project)
admin.site.register(Project_Picture_mobile)
admin.site.register(Project_Picture_web)
admin.site.register(Service)
admin.site.register(Course)
admin.site.register(Section)

admin.site.register(Student_Project_Request)
admin.site.register(Student_Course_Request)
admin.site.register(Company_Request)
