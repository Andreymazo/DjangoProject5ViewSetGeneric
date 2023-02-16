from rest_framework import serializers

from spa.models import Lesson, Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name',
                  'preview',
                  'description',
                )


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('name',
                  'preview',
                  'description',
                  'reference'
                  )

