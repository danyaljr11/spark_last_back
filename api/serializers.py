from rest_framework import serializers
from .models import *


class Member_Serializer_Web(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['pk', 'member_name', 'member_picture_web', 'member_position', 'member_desc', 'member_skills']


class Member_Serializer_Mobile(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['pk', 'member_name', 'member_picture_mobile', 'member_position', 'member_desc', 'member_skills']


class Section_Serializer_Web(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['pk', 'section_name', 'section_image_web']


class Section_Serializer_Mobile(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['pk', 'section_name', 'section_image_mobile']


class Project_Picture_Serializer_Web(serializers.ModelSerializer):
    class Meta:
        model = Project_Picture_web
        fields = ['image']


class Project_Picture_Serializer_Mobile(serializers.ModelSerializer):
    class Meta:
        model = Project_Picture_mobile
        fields = ['image']


class Project_Serializer_Web(serializers.ModelSerializer):
    web_pictures = Project_Picture_Serializer_Web(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['pk', 'project_name', 'project_field', 'project_link', 'project_desc', 'web_pictures']


class Project_Serializer_Mobile(serializers.ModelSerializer):
    mobile_pictures = Project_Picture_Serializer_Mobile(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['pk', 'project_name', 'project_field', 'project_link', 'project_desc', 'mobile_pictures']


class Student_Project_Serializer_Web(serializers.ModelSerializer):
    web_pictures = Project_Picture_Serializer_Web(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['pk', 'project_name', 'project_field', 'project_desc', 'web_pictures']


class Student_Project_Serializer_Mobile(serializers.ModelSerializer):
    mobile_pictures = Project_Picture_Serializer_Mobile(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['pk', 'project_name', 'project_field', 'project_desc', 'mobile_pictures']


class Service_Serializer_Mobile_all(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['pk', 'service_name', 'service_icon', 'service_picture_mobile', 'service_description']


class Service_Serializer_Web(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['pk', 'service_name', 'service_icon', 'service_picture_web', 'service_description']


class Service_Serializer_Mobile_short(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_name', 'service_icon']


class Course_Serializer_Web(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['pk', 'name', 'image_web', 'desc', 'teacher', 'time']


class Course_Serializer_Mobile(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['pk', 'name', 'image_mobile', 'desc', 'teacher', 'time']


class Student_Project_Request_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Project_Request
        fields = ['id', 'name', 'university_name', 'phone', 'desc', 'project']


class Student_Course_Request_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Course_Request
        fields = ['id', 'name', 'phone', 'desc', 'course']


class Company_Request_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Company_Request
        fields = ['id', 'agent_name', 'company_name', 'email', 'phone', 'desc', 'service']


class ProjectSerializer2(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()
    project_desc = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['pk', 'project_name', 'project_field', 'project_desc', 'first_image']

    def get_first_image(self, obj):
        # Get the first image related to the project
        first_image = Project_Picture_web.objects.filter(project=obj).first()
        if first_image:
            # Get the request from the serializer's context
            request = self.context.get('request')
            # Return the URL of the first image
            return request.build_absolute_uri(first_image.image.url)
        else:
            return None

    def get_project_desc(self, obj):
        # Initialize an empty dictionary for the sliced descriptions
        sliced_desc = {}

        # Iterate over each language version in the project_desc field
        for lang, desc in obj.project_desc.items():
            # Check if the description is a string
            if isinstance(desc, str):
                # Slice the description to the first 20 characters and add it to the sliced_desc dictionary
                sliced_desc[lang] = desc[:20]
            else:
                # If the description is not a string, handle the error appropriately
                sliced_desc[lang] = None

        # Return the sliced_desc dictionary
        return sliced_desc


class NotificationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    text = serializers.CharField()
    icon = serializers.CharField(max_length=255, required=False)




