from rest_framework import generics, mixins, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class service_list_mobile(generics.GenericAPIView):
    queryset = Service.objects.none()

    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        services_serializer = Service_Serializer_Mobile_short(services, many=True)
        return Response({
            'services': services_serializer.data,
        })


class service_pk_mobile(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Service.objects.all()
    serializer_class = Service_Serializer_Mobile_all

    def get(self, request, pk):
        return self.retrieve(request)


class service_list_web(generics.GenericAPIView):
    queryset = Service.objects.all()
    serializer_class = Service_Serializer_Web

    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        services_serializer = Service_Serializer_Web(services, many=True)
        return Response({
            'services': services_serializer.data,
        })


class member_list_mobile(generics.GenericAPIView):
    queryset = Member.objects.none()  # Required for Django Rest Framework

    def get(self, request, *args, **kwargs):
        members = Member.objects.all()
        member_serializer = Member_Serializer_Mobile(members, many=True)
        return Response({
            'members': member_serializer.data,
        })


class member_list_web(generics.GenericAPIView):
    queryset = Member.objects.none()  # Required for Django Rest Framework

    def get(self, request, *args, **kwargs):
        members = Member.objects.all()
        member_serializer = Member_Serializer_Web(members, many=True)
        return Response({
            'members': member_serializer.data,
        })


class our_projects_mobile(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Project.objects.none()

    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(is_company=True)
        project_serializer = Project_Serializer_Mobile(projects, many=True)

        return Response({
            'company_project': project_serializer.data,
        })


class Student_Services_mobile(APIView):
    def get(self, request, pk, format=None):
        # Filter the projects and courses based on the attributes
        projects = Project.objects.filter(is_company=False)
        pk = self.kwargs.get('pk')
        section = Section.objects.get(pk=pk)
        courses = Course.objects.filter(section=section)

        # Serialize the data
        project_serializer = Project_Serializer_Mobile(projects, many=True)
        course_serializer = Course_Serializer_Mobile(courses, many=True)

        # Prepare the data for the response
        data = {
            'projects': project_serializer.data,
            'courses': course_serializer.data,
        }

        # Return a JSON response
        return Response(data)


class sections_list_web(generics.GenericAPIView):
    queryset = Section.objects.none()

    def get(self, request, *args, **kwargs):
        sections = Section.objects.all()
        sections_serializer = Section_Serializer_Web(sections, many=True)
        return Response({
            'sections': sections_serializer.data,
        })


class sections_list_mobile(generics.GenericAPIView):
    queryset = Section.objects.none()

    def get(self, request, *args, **kwargs):
        sections = Section.objects.all()
        sections_serializer = Section_Serializer_Mobile(sections, many=True)
        return Response({
            'sections': sections_serializer.data,
        })


class CompanyRequestCreateView(CreateModelMixin, generics.GenericAPIView):
    queryset = Company_Request.objects.all()
    serializer_class = Company_Request_Serializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        agent_name = serializer.validated_data['agent_name']
        company_name = serializer.validated_data['company_name']
        service_id = serializer.validated_data['service'].id

        # Check for duplicate requests
        duplicate_requests = Company_Request.objects.filter(agent_name=agent_name, company_name=company_name,
                                                            service_id=service_id)

        if duplicate_requests.exists():
            raise serializers.ValidationError("Duplicate request")

        # Save the request
        serializer.save()


class StudentCourseRequest(CreateModelMixin, generics.GenericAPIView):
    queryset = Student_Course_Request.objects.all()
    serializer_class = Student_Course_Request_Serializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        name = serializer.validated_data['name']
        phone = serializer.validated_data['phone']
        course = serializer.validated_data['course'].id

        # Check for duplicate requests
        duplicate_requests = Student_Course_Request.objects.filter(name=name, phone=phone, course=course)

        if duplicate_requests.exists():
            raise serializers.ValidationError("Duplicate request")

        # Save the request
        serializer.save()


class StudentProjectRequest(CreateModelMixin, generics.GenericAPIView):
    queryset = Student_Project_Request.objects.all()
    serializer_class = Student_Project_Request_Serializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        name = serializer.validated_data['name']
        phone = serializer.validated_data['phone']
        project = serializer.validated_data['project'].id

        # Check for duplicate requests
        duplicate_requests = Student_Project_Request.objects.filter(name=name, phone=phone, project=project)

        if duplicate_requests.exists():
            raise serializers.ValidationError("Duplicate request")

        # Save the request
        serializer.save()


class StudentProjects(APIView):
    def get(self, request, pk, format=None):
        # Filter the projects based on the attributes
        projects = Project.objects.filter(is_company=False)
        pk = self.kwargs.get('pk')
        section = Section.objects.get(pk=pk)

        # Serialize the data
        project_serializer = Project_Serializer_Web(projects, many=True)

        # Prepare the data for the response
        data = {
            'projects': project_serializer.data,
        }

        # Return a JSON response
        return Response(data)


class StudentCourses(APIView):
    def get(self, request, pk, format=None):
        # Filter the courses based on the attributes
        pk = self.kwargs.get('pk')
        section = Section.objects.get(pk=pk)
        courses = Course.objects.filter(section=section)

        # Serialize the data
        course_serializer = Course_Serializer_Web(courses, many=True)

        # Prepare the data for the response
        data = {
            'courses': course_serializer.data,
        }

        # Return a JSON response
        return Response(data)


class OurProjectsList(APIView):
    def get(self, request):
        projects = Project.objects.filter(is_company=True)
        serializer = ProjectSerializer2(projects, many=True, context={'request': request})
        return Response(serializer.data)


class OurProjectDetails(generics.RetrieveAPIView):
    queryset = Project.objects.filter(is_company=True)
    serializer_class = Project_Serializer_Web
    lookup_field = 'pk'


class FCMDeviceView(APIView):
    def post(self, request, format=None):
        serializer = FCMDeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
