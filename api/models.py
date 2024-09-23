from django.db import models
import firebase_admin
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice
from firebase_admin import credentials
from firebase_admin.messaging import Message, Notification

#cred = credentials.Certificate('serviceAccountKey.json')
#firebase_admin.initialize_app(cred)


#cred = credentials.Certificate('/home/sparkeng/spark_last_back/serviceAccountKey.json')
#firebase_admin.initialize_app(cred)

# Create your models here.


class Member(models.Model):
    member_name = models.JSONField(null=True)  # اسم الموظف
    member_picture_mobile = models.ImageField(upload_to='images/mobile_images/member_images/',max_length= 200)  # صورة الموظف
    member_picture_web = models.ImageField(upload_to='images/web_images/member_images/',max_length= 200)  # صورة الموظف
    member_position = models.JSONField(null=True)  # منصب الموظف
    member_desc = models.JSONField(null=True)  # معلومات الموظف
    member_skills = models.JSONField(null=True)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.member_name.get('EN', 'no name')


class Section(models.Model):
    name = models.JSONField(max_length=30)
    section_image_mobile = models.ImageField(upload_to='images/mobile_images/section_images/',max_length= 200)  # صورة القسم
    section_image_web = models.ImageField(upload_to='images/web_images/section_images/',max_length= 200)  # صورة القسم

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name.get('EN', 'no name')


@receiver(post_save, sender=Section)
def send_notification_sections(sender, instance, created, **kwargs):
    if created:
        message = Message(
            data={"screen": "section",
                  "pk": str(instance.pk)
                  },
            notification=Notification(
                title="New Section Added",
                body=instance.name.get('EN'),
            ),
        )
        devices = FCMDevice.objects.all()
        devices.send_message(message)


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
        return self.project_name.get('EN', 'no name')


class Project_Picture_mobile(models.Model):
    picture_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/mobile_images/project_images/',max_length= 200)
    project = models.ForeignKey('Project', related_name='mobile_pictures', on_delete=models.CASCADE)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.picture_title


class Project_Picture_web(models.Model):
    picture_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/web_images/project_images/',max_length= 200)
    project = models.ForeignKey('Project', related_name='web_pictures', on_delete=models.CASCADE)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.picture_title


class Service(models.Model):
    name = models.JSONField()
    service_icon = models.ImageField(upload_to='images/service_icons/',max_length= 200)
    service_picture_mobile = models.ImageField(upload_to='images/mobile_images/service_images/',max_length= 200)
    service_picture_web = models.ImageField(upload_to='images/web_images/service_images/',max_length= 200)
    service_description = models.JSONField()

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name.get('EN', 'no name')


@receiver(post_save, sender=Service)
def send_notification_services(sender, instance, created, **kwargs):
    if created:
        message = Message(
            data={"screen": "service",
                  "pk": str(instance.pk)
                  },
            notification=Notification(
                title="New Service Added",
                body=instance.name.get('EN'),
            ),
        )
        devices = FCMDevice.objects.all()
        devices.send_message(message)


class Course(models.Model):
    name = models.JSONField()
    image_mobile = models.ImageField(upload_to='images/mobile_images/course_images/',max_length= 200)
    image_web = models.ImageField(upload_to='images/web_images/course_images/',max_length= 200)
    desc = models.JSONField()
    teacher = models.JSONField()
    time = models.JSONField()
    section = models.ForeignKey('Section', on_delete=models.CASCADE)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.name.get('EN', 'No name')


@receiver(post_save, sender=Course)
def send_notification_courses(sender, instance, created, **kwargs):
    if created:
        message = Message(
            data={"screen": "course",
                  "pk": str(instance.section.pk)
                  },
            notification=Notification(
                title="New Course Added",
                body=instance.name.get('EN'),
            ),
        )
        devices = FCMDevice.objects.all()
        devices.send_message(message)


class Student_Project_Request(models.Model):
    name = models.CharField(max_length=30)
    university_name = models.CharField(max_length=30)
    phone = models.BigIntegerField(default=None)
    desc = models.CharField(max_length=500, default=None)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'phone', 'project')


    def __str__(self):
        return self.name


class Student_Course_Request(models.Model):
    name = models.CharField(max_length=30)
    phone = models.BigIntegerField(default=None)
    desc = models.CharField(max_length=500, default=None)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'phone', 'course')

    def __str__(self):
        return self.name


class Company_Request(models.Model):
    agent_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    desc = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('agent_name', 'company_name', 'service')

    def __str__(self):
        return self.agent_name




