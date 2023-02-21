from rest_framework import serializers
from rest_framework.fields import CharField

from spa.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('name',
                  'preview',
                  'reference',
                  )


class CourseSerializer(serializers.ModelSerializer):
    #lessons_amount = serializers.SerializerMethodField()
    lessons_amount = LessonSerializer(source='smthin', many=True)#CharField(),
        ##, slug_field="name"queryset=Lesson.object.all()
    class Meta:
        model = Course
        fields = ('id',
                  'name',
                  'preview',
                  'description',
                  'lessons_amount'
                )
    # def create(self, validated_data):
    #     validated_data.pop('lessons_amount')
    #     lessons_amount, created = Course.objects.all.get_or_create(name=validated_data["lessons_amount"],)
    #     print(created, 'GGGGGGGGGGG')
    #     new_lessons_amount=Lesson.object.create(lessons_amount=lessons_amount, **validated_data,)
    #     return  new_lessons_amount
    # # #
    # # #
    # #     lessons_amount_data = validated_data.pop('lessons_amount')
    # #     course = Course.objects.create(**validated_data)
    # #     for k in lessons_amount_data:
    # #         # print(k, 'WWWWWWW')
    # #         Lesson.objects.create(course=course, **k)
    # #         print(self.create(), 'FFFFFFFFFF')
    # #         print(course, 'FFFFFFFFFFFF')
    # #     return course
    # #
    # #     lessons_amount = Course.objects.create(lessons_amount_data)
    def get_description(self, instance):
        return Lesson.get_lessons_amount(instance)


