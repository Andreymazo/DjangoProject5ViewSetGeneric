from rest_framework import serializers
from rest_framework.fields import CharField

from spa.models import Lesson, Course, Payment, CustomUser, UserSubscription


class Modelvalidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # if value.get('preview') and '^(?:(?!youtube.com).)*?$' not in value.get('preview'):
        s = value.get('preview')
        result = re.search(r'youtube\.com', str(f'{s}'))
        if result == None:  ##Esli net 'youtube.com' vozvrashaet None
            print('resulttttt', result)
            raise serializers.ValidationError('No such mach')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('smth',
                  'name',
                  'preview',
                  'reference',
                  )

    validators = [Modelvalidator(field='preview')]


import re


class CourseSerializer(serializers.ModelSerializer):
    lessons_amount = serializers.SerializerMethodField()
    # lessons_amount = LessonSerializer(read_only=False, source='smthin', many=True)
    lesson = LessonSerializer(source='smthin', many=True)  # CharField(),

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
        validators = [Modelvalidator(field='preview')]

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
        #     new_lessons_amount=Lesson.object.create(lessons_amount=lessons_amount, **validated_data,)
        #     return  new_lessons_amount
        lessons_amount_data = validated_data.pop('smthin')
        smth = Course.objects.create(**validated_data)
        for k in lessons_amount_data:
            Lesson.objects.create(smth=smth, **k)  ##Zdes course ne vidit
        return smth
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


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ["user", "status", "subscribed_on", ]
