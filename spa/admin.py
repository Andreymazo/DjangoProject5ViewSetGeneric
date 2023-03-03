# from django.contrib import admin
# from django.contrib.admin.forms import AdminPasswordChangeForm
# from django.contrib.auth.admin import UserAdmin
# from forms import CustomUserRegistrationForm
# from django.contrib.auth.forms import UserChangeForm, UserCreationForm
# from pkg_resources import _
from django.contrib.admin import TabularInline

import spa
from spa.models import CustomUser, Course, Lesson \
    # , CustomUserManager

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from .forms import CustomUserRegistrationForm, CustomUserChangeForm


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserRegistrationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('email'),  # 'company''firstname', 'lastname',
    list_filter = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  ##'old_password', 'new_password', 'new_password2'
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        # ('Personal Information', {'fields': ('firstname', 'lastname', 'phone')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password', 'is_staff')}),  ##'password2',
        # ('Personal Information', {'fields': ('firstname', 'lastname', 'phone')}),
        # ('Company Information', {'fields': ('company',)}),
    )

    class Meta:
        model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)


# class MyUserChangeForm(UserChangeForm):##Menyaem adminku dlya Usera
#     class Meta(UserChangeForm.Meta):
#         model = CustomUser
# class MyUserAdmin(UserAdmin):
#     add_form = CustomUserRegistrationForm
#     form = MyUserChangeForm
#
#     list_display = ("email", "is_staff")
#     list_filter = ("is_staff", "is_superuser", "is_active", "groups")
#     search_fields = "email"
#     ordering = ("email",)
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         (_("Personal info"), {"fields": "email"}),
#         (
#             _("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#         (_("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("email", "password1", "password2"),
#             },
#         ),
#     )
#     form = UserChangeForm
#     add_form = UserCreationForm
#     change_password_form = AdminPasswordChangeForm

# filter_horizontal = (
#     "groups",
#     "user_permissions",
# )

# admin.site.register(CustomUser, UserAdmin)
# admin.site.register(CustomUserManager)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['email']#, 'phone', 'avatar', 'city'
# admin.site.register(User)

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'preview', 'description']


admin.site.register(Course)


class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'preview', 'description', 'reference']


admin.site.register(Lesson)

# class MyVideoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'video_tag', 'comment', )
#
#     def video_tag(self, obj):
#         if obj.video:
#             return format_html('<a href="{}">Link to video</a><video height="200px" controls><source src="{}" type="video/mp4"></video>'.format(obj.video.url, obj.video.url))
#     video_tag.short_description = 'Video'
#
# admin.site.register(MyVideo, MyVideoAdmin)
# in temlate:<video width="500px" height="500px" controls>
#      <source src="{{ post.video_file.url }}" type="video/mp4">
# </video>


# from django.contrib import admin

from spa.models import Profile, UserSubscription, Payment

admin.site.register(Profile)


class Profile(admin.ModelAdmin):##TabularInline
    list_display = ['slug']

    prepopulated_fields = {'slug': ('slug',)}  # new






    # raw_id_fields = ("follows",) <- wrong
    # raw_id_fields = ("following_subscription",) # <- probably right, because your m2m relation with `User` table and django use name of that table to name field in `through` mode
admin.site.register(Payment)

admin.site.register(UserSubscription)

list_display = ['slug', 'subscribed_on']
