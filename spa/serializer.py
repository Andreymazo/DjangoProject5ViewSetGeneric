from rest_framework import serializers
from rest_framework.fields import CharField

from spa.models import Lesson, Course, Payment, CustomUser


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('smth',
                    'name',
                
                  'reference',
                  )


class CourseSerializer(serializers.ModelSerializer):
    lessons_amount = serializers.SerializerMethodField()
    # lessons_amount = LessonSerializer(read_only=False, source='smthin', many=True)
    lesson = LessonSerializer(source='smthin', many=True)#CharField(),
        ##, slug_field="name"queryset=Lesson.object.all()
    class Meta:
        model = Course
        fields = ('id',
                  'name',
                  'preview',
                  'description',
                  'lessons_amount',
                  'lesson'
                  )
    def get_lessons_amount(self, instance):
        # print(instance.smthin)
        # lesson_object=Lesson.objects.filter(smth=instance)
        # if lesson_object:
        #     return lesson_object.count()
        # return 0
        return instance.smthin.count()
    def create(self, validated_data):
    #     validated_data.pop('lessons_amount')
    #     lessons_amount, created = Course.objects.all.get_or_create(name=validated_data["lessons_amount"],)
    #     print(created, 'GGGGGGGGGGG')
    #     new_lessons_amount=Lesson.object.create(lessons_amount=lessons_amount, **validated_data,)
    #     return  new_lessons_amount
    # # #
    # # #
        lessons_amount_data = validated_data.pop('smthin')

        # print(lessons_amount_data)
        smth = Course.objects.create(**validated_data)
        # print('COURSE course = ', smth)
        for k in lessons_amount_data:
            # print(k, 'WWWWWWW')
            # print(smth, 'FFFFFFFFFFFF')
            Lesson.objects.create(smth=smth, **k)##Zdes course ne vidit
            # print('FFFFFFFFFF')##self.create(),

        return smth
    # #
    # #     lessons_amount = Course.objects.create(lessons_amount_data)
    # def get_description(self, instance):
    #     return Lesson.get_lessons_amount(instance)

# def get_serializer_class(self):
#     if self.request.user.is_staff:
#         return FullAccountSerializer
#     return BasicAccountSerializer

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'user_id',
            'date_of_payment',
            'sum_of_payment'
        ]
        # fields = '__all__'
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
class CustomUserPaySerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True, source='payment_set')

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'payment'
        ]

