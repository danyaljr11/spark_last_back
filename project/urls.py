from django.contrib import admin
from api import views
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest/service_list_mobile/', views.service_list_mobile.as_view()),
    path('rest/service_pk_mobile/<int:pk>', views.service_pk_mobile.as_view()),
    path('rest/service_list_web/', views.service_list_web.as_view()),
    path('rest/member_list_mobile/', views.member_list_mobile.as_view()),
    path('rest/member_list_web/', views.member_list_web.as_view()),
    path('rest/our_projects_mobile/', views.our_projects_mobile.as_view()),
    path('rest/sections_list_web/', views.sections_list_web.as_view()),
    path('rest/sections_list_mobile/', views.sections_list_mobile.as_view()),
    path('rest/student_project_request/', views.StudentProjectRequest.as_view()),
    path('rest/student_course_request/', views.StudentCourseRequest.as_view()),
    path('rest/company_request/', views.CompanyRequestCreateView.as_view()),
    path('rest/Student_Services_mobile/<int:pk>', views.Student_Services_mobile.as_view()),
    path('rest/student_projects/<int:pk>', views.StudentProjects.as_view()),
    path('rest/student_courses/<int:pk>', views.StudentCourses.as_view()),
    path('rest/our_projects_list/', views.OurProjectsList.as_view()),
    path('rest/our_project_details/<int:pk>', views.OurProjectDetails.as_view()),
    path('send-notification/', views.SendNotificationAPIView.as_view()),

]

