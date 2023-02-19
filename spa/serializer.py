from rest_framework import serializers

from spa.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('name',
                  'preview',
                  'description',
                  'reference',
                  )


class CourseSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    lessons_amount = LessonSerializer(source='description_set', many=True)
    class Meta:
        model = Course
        fields = ('id',
                  'name',
                  'preview',
                  'description',
                  'lessons_amount'
                )
    def create(self, validated_data):
        lessons_amount_data = validated_data.pop('lessons_amount')

        course = Course.objects.create(**validated_data)
        for k in lessons_amount_data:
            Lesson.objects.create(course=course, **k)
        return course

        # lessons_amount = Course.objects.create(lessons_amount_data)
    def get_lessons_amount(self, instance):
        return Lesson.get_lessons_amount(instance)



