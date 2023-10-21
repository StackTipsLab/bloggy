from rest_framework import generics

from bloggy.models.course import Course
from bloggy_api.serializers import CourseSerializer


class CoursesAPIView(generics.ListAPIView):
    queryset = Course.objects.filter(publish_status="LIVE") \
        .order_by("-published_date")
    serializer_class = CourseSerializer
