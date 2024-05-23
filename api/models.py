from django.db import models
import firebase_admin
from fcm_django.models import FCMDevice
from firebase_admin import credentials
from firebase_admin.messaging import Message
from django.db.models.signals import post_save
from django.dispatch import receiver

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)


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
        return self.member_name.get('EN', 'no name')


class Section(models.Model):
    section_name = models.CharField(max_length=30)
    section_image_mobile = models.ImageField(upload_to='mobile_images/section_images/')  # صورة القسم
    section_image_web = models.ImageField(upload_to='web_images/section_images/')  # صورة القسم

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.section_name


@receiver(post_save, sender=Section)
def send_notification_courses(sender, instance, created, **kwargs):
    if created:
        devices = FCMDevice.objects.all()
        for device in devices:
            # Determine the language for the notification
            language = device.language if hasattr(device, 'language') else 'EN'

            # Construct the notification message based on the language
            if language == 'AR':
                title = "تم إضافة قسم جديد"
                body = instance.name.get('AR', 'اسم القسم غير متوفر')
            else:  # Default to English
                title = "A New Section Added"
                body = instance.name.get('EN', 'Section name not available')

            # Define the JSON message format
            message_data = {
                "title": title,
                "body": body,
                "screen": "screen_name",  # Replace with your actual screen name
                "note": "Section"  # Replace with your actual notification type
            }

            # Send the message
            device.send_message(data=message_data)


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
        return self.service_name.get('EN', 'no name')


@receiver(post_save, sender=Service)
def send_notification_courses(sender, instance, created, **kwargs):
    if created:
        devices = FCMDevice.objects.all()
        for device in devices:
            # Determine the language for the notification
            language = device.language if hasattr(device, 'language') else 'EN'

            # Construct the notification message based on the language
            if language == 'AR':
                title = "تم إضافة خدمة جديدة"
                body = instance.name.get('AR', 'اسم الخدمة غير متوفر')
            else:  # Default to English
                title = "A New Service Added"
                body = instance.name.get('EN', 'Service name not available')

            # Define the JSON message format
            message_data = {
                "title": title,
                "body": body,
                "screen": "screen_name",  # Replace with your actual screen name
                "note": "Service"  # Replace with your actual notification type
            }

            # Send the message
            device.send_message(data=message_data)


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
        return self.name.get('EN', 'No name')


@receiver(post_save, sender=Course)
def send_notification_courses(sender, instance, created, **kwargs):
    if created:
        devices = FCMDevice.objects.all()
        for device in devices:
            # Determine the language for the notification
            language = device.language if hasattr(device, 'language') else 'EN'

            # Construct the notification message based on the language
            if language == 'AR':
                title = "تم إضافة كورس جديد"
                body = instance.name.get('AR', 'اسم الدورة غير متوفر')
            else:  # Default to English
                title = "A New Course Added"
                body = instance.name.get('EN', 'Course name not available')

            # Define the JSON message format
            message_data = {
                "title": title,
                "body": body,
                "screen": "screen_name",  # Replace with your actual screen name
                "note": "Course"  # Replace with your actual notification type
            }

            # Send the message
            device.send_message(data=message_data)


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


class FCMDevice(models.Model):
    registration_id = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    language = models.CharField(max_length=10, choices=[('EN', 'English'), ('AR', 'Arabic')])

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.registration_id
