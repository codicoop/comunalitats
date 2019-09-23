from django.contrib import admin

from .models import Room, Reservation
from .forms import RoomForm, ReservationForm
from coopolis.models import User
from cc_courses.models import CoursePlace


class RoomAdmin(admin.ModelAdmin):
    form = RoomForm
    list_display = ('name', 'color', 'capacity',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "place":
            kwargs["queryset"] = CoursePlace.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Room, RoomAdmin)


class ReservationAdmin(admin.ModelAdmin):
    class Media:
        # Grappelli was not even loading this file (maybe jquery did, internally?)
        # Adding it that way (and having the right order in INSTALLED_APPS injects the file,
        # and then the time pickers use it.
        js = ("grappelli/js/jquery.grp_timepicker.js",)

    form = ReservationForm
    readonly_fields = ('created_by', 'created',)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Reservation, ReservationAdmin)
