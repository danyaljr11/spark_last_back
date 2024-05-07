from django.db import models


# Create your models here.


class Member(models.Model):
    member_name = models.JSONField(null=True)  # اسم الموظف
    member_picture_mobile = models.ImageField(upload_to='mobile_images/member_images/')  # صورة الموظف
    member_picture_web = models.ImageField(upload_to='web_images/member_images/')  # صورة الموظف
    member_position = models.JSONField(null=True)  # منصب الموظف
    member_desc = models.JSONField(null=True)  # معلومات الموظف
    member_skills = models.JSONField(null=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.member_name.__str__()


class Section(models.Model):
    section_name = models.CharField(max_length=30)
    section_image_mobile = models.ImageField(upload_to='mobile_images/section_images/')  # صورة القسم
    section_image_web = models.ImageField(upload_to='web_images/section_images/')  # صورة القسم

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.section_name


class Project(models.Model):
    project_field = models.JSONField(null=True)  # نوع المشروع ويب تطبيق كذا
    project_name = models.JSONField(null=True)  # اسم المشروع
    project_link = models.URLField(null=True, blank=True)  # رابط المشروع
    project_desc = models.JSONField(null=True)  # وصف المشروع
    is_company = models.BooleanField(default=False)
    section = models.ForeignKey('Section', on_delete=models.CASCADE)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.project_name.__str__()


class Project_Picture_mobile(models.Model):
    picture_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='mobile_images/project_images/')
    project = models.ForeignKey('Project', related_name='mobile_pictures', on_delete=models.CASCADE)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.picture_title


class Project_Picture_web(models.Model):
    picture_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='web_images/project_images/')
    project = models.ForeignKey('Project', related_name='web_pictures', on_delete=models.CASCADE)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.picture_title


class Service(models.Model):
    service_name = models.JSONField()
    service_icon = models.ImageField(upload_to='images/service_icons/')
    service_picture_mobile = models.ImageField(upload_to='mobile_images/service_images/')
    service_picture_web = models.ImageField(upload_to='web_images/service_images/')
    service_description = models.JSONField()

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.service_name.__str__()


class Course(models.Model):
    name = models.JSONField()
    image_mobile = models.ImageField(upload_to='mobile_images/course_images/')
    image_web = models.ImageField(upload_to='web_images/course_images/')
    desc = models.JSONField()
    teacher = models.JSONField()
    time = models.JSONField()
    section = models.ForeignKey('Section', on_delete=models.CASCADE)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name.__str__()


class Student_Project_Request(models.Model):
    name = models.CharField(max_length=30)
    university_name = models.CharField(max_length=30)
    phone = models.BigIntegerField(default=None)
    desc = models.CharField(max_length=500, default=None)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name


class Student_Course_Request(models.Model):
    name = models.CharField(max_length=30)
    phone = models.BigIntegerField(default=None)
    desc = models.CharField(max_length=500, default=None)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Company_Request(models.Model):
    agent_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    desc = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return self.agent_name
