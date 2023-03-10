from django.core.management import BaseCommand

from spa.models import Course, CustomUser, Profile


class Command(BaseCommand):

    def handle(self, *args, **options):
        prfles = ['foreign_papa', 'Mike', 'Piter']##Sozdaem 3 profila na 3 userov

        # index=1
        # for i in prfles:
        #     profile = Profile.objects.create(
        #         user_id=index,
        #         title=i,
        #     )
        #     index+=1
        #     profile.save()
        profile = Profile.objects.create(
                    email="andreymazo@mail.ru",
                    user_id=1,
                    title="foreign_papa",
                )
        profile.save()


        profile = Profile.objects.create(
            email='foreipa@foreipa.ru',
            user_id=2,
            title="Mike",
        )
        profile.save()

        profile = Profile.objects.create(
            email='anderymazo22@mail.ru',
            user_id=3,
            title="Piter",
        )
        profile.save()

        ######################################################################################
        emails = ['2andreymazo@mail.ru', 'foreipa@foreipa.ru', 'anderymazo22@mail.ru']
        # profile = Profile.objects.all().get(pk=1).email
        # # print(profile)
        # profile ='foreipa@foreipa.ru'
        # profile.save()
        # Profile.objects.all().get(pk=1).update(email='foreipa@foreipa.ru')
        # Profile.objects.all().get(pk=1).save()
        # print(Profile.objects.all().get(pk=1).email)
        # print(a)
        # a.update(
        #         email='foreipa@foreipa.ru'
        #     )

        # a.save()
        # for i in emails:
        #
        #     profile = Profile.objects.update(
        #         email=i
        #     )
        #     profile.save()  ###django.db.utils.IntegrityError: UNIQUE constraint failed: spa_profile.email

#####################################         Update v serialezatore
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, unique=True)
#     phone_number = models.CharField(blank=True,null=True,max_length=20)
#     access_token = models.CharField(blank=True,null=True,max_length=140)
#     email_sub = models.BooleanField(default=False)
#
# class UserSerializer(UserDetailsSerializer):
# 	phone_number = serializers.CharField(source="userprofile.phone_number")
# 	access_token = serializers.CharField(allow_blank=True,source="userprofile.access_token")
# 	email_sub = serializers.BooleanField(source="userprofile.email_sub")
#
#
# 	class Meta(UserDetailsSerializer.Meta):
# 		fields = ['pk', 'username', 'email', 'first_name', 'last_name'] + \
# 			[f.name for f in UserProfile._meta.get_fields()]
# 		del fields[fields.index('user')]
#
#
# 	def update(self, instance, validated_data):
# 		raise_errors_on_nested_writes('update', self, validated_data)
# 		info = model_meta.get_field_info(instance)
# 		profile = instance.userprofile
# 		p_info = model_meta.get_field_info(profile)
#
# 		for attr, value in validated_data.items():
# 			if attr == 'userprofile':
# 				for attr2, value2 in value.items():
# 					setattr(profile, attr2, value2)
#
# 			elif attr in info.relations and info.relations[attr].to_many:
# 				field = getattr(instance, attr)
# 				field.set(value)
# 			else:
# 				setattr(instance, attr, value)
# 		instance.save()
# 		profile.save()
#
# 		return instance
