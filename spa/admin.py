from django.contrib import admin

from spa.models import User, Course, Lesson


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'avatar', 'city']
admin.site.register(User)

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