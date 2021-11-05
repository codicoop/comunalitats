from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class ActivityPollAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('styles/grappelli-change-list-width-fixed.css', 'styles/grappelli-change-list-hide-total.css')
        }

    # IMPORTANT: Evita que el camp User arribi a mostrar-se mai per preservar l'anonimat de l'enquesta.
    list_display = (
        # Organització
        'duration', 'hours', 'information', 'on_schedule', 'included_resources', 'space_adequation',
        # Continguts
        'contents',
        # Metodologia
        'methodology_fulfilled_objectives', 'methodology_better_results', 'participation_system',
        # Valoració de la persona formadora
        'teacher_has_knowledge', 'teacher_resolved_doubts', 'teacher_has_communication_skills',
        # Utilitat del curs
        'expectations_satisfied', 'adquired_new_tools', 'met_new_people', 'wanted_start_cooperative',
        'wants_start_cooperative_now',
        # Valoració global
        'general_satisfaction', 'also_interested_in', 'heard_about_it', 'comments'
    )
    list_per_page = 500

    """Disables all editing capabilities."""
    list_display_links = None

    def get_fields(self, request, obj=None):
        return self.list_display

    def get_actions(self, request):
        actions = super().get_actions(request)
        del_action = "delete_selected"
        if del_action in actions:
            del actions[del_action]
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_change_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        pass

    def delete_model(self, request, obj):
        pass

    def save_related(self, request, form, formsets, change):
        pass

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return HttpResponseRedirect(reverse_lazy('admin:index'))
