from rest_framework import serializers
from rest_framework.fields import CharField

from spa.models import Lesson, Course, Payment, CustomUser, UserSubscription, Profile, STATUS_START


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
        fields = ('__all__'
                  # 'smth',
                  #           'name',
                  #           "description",
                  #           'preview',
                  # 'reference',
                  )

    # validators = [Modelvalidator(field='preview')]


import re
from spa.tasks import course_check


class CourseSerializer(serializers.ModelSerializer):
    lessons_amount = serializers.SerializerMethodField()
    # lessons_amount = LessonSerializer(read_only=False, source='smthin', many=True)
    lesson = LessonSerializer(source='smthin',  #####Komment 39,40,50 str chtobi update Course prohodil
                              many=True)  # , read_only=True)  # CharField(),##many=False,read_only=True

    ##, slug_field="name"queryset=Lesson.object.all()
    has_subscrpt = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id',
            'name',
            'preview',
            'description',
            'pro_file',
            'lessons_amount',
            'lesson',
            "has_subscrpt"
        )
        # validators = [Modelvalidator(field='preview')]

    def get_lessons_amount(self, instance):
        return instance.smthin.count()

    def create(self, validated_data):
        lesson_data = validated_data.pop('smthin')
        # print(lesson_data)
        smth = Course.objects.create(**validated_data)
        for k in lesson_data:
            Lesson.objects.create(smth=smth, **k)  ##Zdes course ne vidit
        return smth

    # #     lessons_amount = Course.objects.create(lessons_amount_data)
    # def get_description(self, instance):
    #     return Lesson.get_lessons_amount(instance)

    def update(self, instance, validated_data):  ###Pishen explicit update method
        # print('____________----------=========', self.instance.pk)

        # validated_data.pop("id", None)
        # return super().update(self, instance, validated_data)
        ###############Ot Olega, povtorit create
        # https://docs.djangoproject.com/en/4.1/ref/models/querysets/#update-or-create
        # create_or_update

        #         # Update the  instance

        #         #  course_mapping = {course.id: course for course in instance}
        #         # data_mapping = {item['id']: item for item in validated_data}
        #         # for i,k in book_mapping:
        #         # print('pppppppppppppp', course_mapping)
        #
        #         # print(instance)##Python To chto bilo

        #         # print(validated_data['smthin'])##Python22 To chto prihodit
        if instance.name != validated_data['name']:
            instance.name = validated_data['name']
            UserSubscription.objects.all().filter(pk=self.instance.pk).first().status_send = STATUS_START
        if instance.name != validated_data['preview']:
            instance.preview = validated_data['preview']
            UserSubscription.objects.all().filter(pk=self.instance.pk).first().status_send = STATUS_START
        if instance.name != validated_data['description']:
            instance.description = validated_data['description']
            UserSubscription.objects.all().filter(pk=self.instance.pk).first().status_send = STATUS_START
        if instance.name != validated_data['pro_file']:
            instance.pro_file = validated_data['pro_file']
            UserSubscription.objects.all().filter(pk=self.instance.pk).first().status_send = STATUS_START

        a = UserSubscription.objects.all().filter(pk=self.instance.pk).first().status_send
        print(a)

        # for i, k in validated_data.items():
        #     # setattr(instance, attr, value)
        #     # print(k)##i --- name, preview, description, smthin##k ---- Python33 youtube.comm very very much of smth [OrderedDict([('name', 'Python for start')])]
        #     self.instance.i = k

        instance.save()
        return instance

    def _user(self):
        if self.context.get('request'):
            return self.context['request'].user.profile
        return None  ##Polzovatel ne aftorizovan

    def get_has_subscrpt(self, instance):
        # Profile.objects.get
        return instance.usersubscription_set.filter(profile=self._user()).exists()


# def get_serializer_class(self):
#     if self.request.user.is_staff:
#         return FullAccountSerializer
#     return BasicAccountSerializer

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('__all__')
        # [
        #     'pro_filee',
        #     'date_of_payment',
        #     'sum_of_payment'
        # ]
        # '__all__'


from django.contrib.auth.hashers import make_password


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        # fields = ('email', 'username', 'refreshToken', 'password')
###########################################  instance.is_active = True  ######################3
    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #
    #     # Adding the below line made it work for me.
    #     instance.is_active = True
    #     if password is not None:
    #         # Set password does the hash, so you don't need to call make_password
    #         instance.set_password(password)
    #     instance.save()
    #     return instance

        # def validate_password(self, value: str) -> str:
        #     """
        #     Hash value passed by user.
        #
        #     :param value: password of a user
        #     :return: a hashed version of the password
        #     """
        #     return make_password(value)


    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #
    #     # Adding the below line made it work for me.
    #     instance.is_active = True
    #     if password is not None:
    #         # Set password does the hash, so you don't need to call make_password
    #         instance.set_password(password)
    #     instance.save()
    #     return instance
    #
    # def validate_password(self, value: str) -> str:
    #     """
    #     Hash value passed by user.
    #
    #     :param value: password of a user
    #     :return: a hashed version of the password
    #     """
    #     return make_password(value)


class CustomUserPaySerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True, source='payment_set')

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'payment'
        ]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    # has_subscrpt_curr_user = serializers.SerializerMethodField()
    class Meta:
        model = UserSubscription
        fields = ["id", "course_subscribe", "lesson_subscribe", "profile", "status", "subscribed_on", "period"]
    # def get_has_subscrpt_curr_user(self):


class ProfileSerializer(serializers.ModelSerializer):
    subscription_info = UserSubscriptionSerializer(source='usersubscription_set', many=True)

    # email = CustomUserSerializer(source="customuser_set", many=False, read_only=True)
    def create(self, validated_data):
        profile_amount_data = validated_data.pop('profile', [])
        profile = UserSubscription.objects.create(**validated_data)
        for k in profile_amount_data:
            Profile.objects.create(profile=profile, **k)
        return profile

    class Meta:
        model = Profile
        fields = ["email", "user", "slug", "following_payment", "subscription_info"]

    # def create(self, validated_data):
    #         profile_data = validated_data.pop('email')
    #         email = Profile.objects.create(**validated_data)
    #         CustomUser.objects.create(email=email, **profile_data)
    #
    #         return email
    # def update(self, instance, validated_data):
    #     instance.email = validated_data["email"]##KeyError: 'email'
    #     instance.user = validated_data["user"]
    #     instance.slug = validated_data["slug"]
    #     instance.following_subscription = ["following_subscription"]
    #     instance.following_payment = ["following_payment"]
    #     instance.subscription_info = ["subscription_info"]
    #     # for i, k in validated_data.items():
    #     #     # setattr(instance, attr, value)
    #     #     # print(k)##i --- name, preview, description, smthin##k ---- Python33 youtube.comm very very much of smth [OrderedDict([('name', 'Python for start')])]
    #     #     self.instance.i = k
    #     instance.save()
    # return instance
    # def update(self, instance, validated_data):
    #     profile_data = validated_data.pop('userprofile')
    #     profile = instance.userprofile
    #
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()
    #
    #     profile.foo = profile_data.get('foo', profile.foo)
    #     profile.bar = profile_data.get('bar', profile.bar)
    #     profile.save()
    #
    #     return instance
