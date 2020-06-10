from django.contrib import admin
from django.db.models import Count, Sum, Q, When
from django.db.models.functions import Coalesce


class ProjectsFollowUpAdmin(admin.ModelAdmin):
    """
    Inspired in: https://medium.com/@hakibenita/how-to-turn-django-admin-into-a-lightweight-dashboard-a0e0bbf609ad
    """
    change_list_template = 'admin/projects_follow_up.html'
    show_full_result_count = False
    list_display = ('name', )
    list_per_page = 99999

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        query = {
            'members_h': Count('stages__involved_partners',
                             filter=Q(stages__involved_partners__gender='MALE'), distinct=True),
            'members_d': Count('stages__involved_partners',
                               filter=Q(stages__involved_partners__gender='FEMALE'), distinct=True),
            'members_total': Count('stages__involved_partners', distinct=True),
            'acollida_hores': Sum('stages__hours', filter=Q(stages__stage_type=1)),
            'acollida_certificat':
                Count('stages__scanned_certificate',
                      filter=Q(stages__stage_type=1) & Q(stages__scanned_certificate__isnull=False)),
            'proces_hores': Sum('stages__hours', filter=Q(stages__stage_type=2)),
            'proces_certificat':
                Count('stages__scanned_certificate',
                      filter=Q(stages__stage_type=2) & Q(stages__scanned_certificate__isnull=False)),
            'constitucio_hores': Sum('stages__hours', filter=Q(stages__stage_type=6)),
            'constitucio_certificat':
                Count('stages__scanned_certificate',
                      filter=Q(stages__stage_type=6) & Q(stages__scanned_certificate__isnull=False)),
            'consolidacio_hores': Sum('stages__hours', filter=Q(stages__stage_type__in=[7, 8])),
            'consolidacio_certificat':
                Count('stages__scanned_certificate',
                      filter=Q(stages__stage_type__in=[7, 8]) & Q(stages__scanned_certificate__isnull=False)),
        }
        #     'total_to_pay': Sum('enrolled_activities__price'),
        #     'total_grants_requested':
        #         Count('activityenrolled__grant_requested',
        #               filter=Q(activityenrolled__grant_requested=True),
        #               distinct=True),
        #     'total_grants_obtained':
        #         Sum('activityenrolled__payments__amount', filter=Q(activityenrolled__payments__method='B')),
        #     'total_to_pay_after_grants':
        #         Sum('enrolled_activities__price') -
        #         Coalesce(
        #             Sum('activityenrolled__payments__amount', filter=Q(activityenrolled__payments__method='B')),
        #             0
        #         ),
        #     'total_payments_without_grants':
        #         Sum('activityenrolled__payments__amount', filter=~Q(activityenrolled__payments__method='B')),
        #     'to_pay':
        #         Sum('enrolled_activities__price') -
        #         Coalesce(Sum('activityenrolled__payments__amount'), 0),
        # }

        # Annotate adds columns to each row with the sum or calculations of the row:
        response.context_data['rows'] = list(
            qs.annotate(**query)
        )

        # Normally it should be easier to call aggregate to have the totals, but given how complex is it to combine
        # with the ORM filters, I opted for filling the values like this.
        # The original version was: qs.aggregate(**query)
        totals = dict(
            total_members_h=0,
            total_members_d=0,
            total_members_total=0,
            total_acollida_hores=0,
            total_acollida_certificat=0,
            total_proces_hores=0,
            total_proces_certificat=0,
            total_constitucio_hores=0,
            total_constitucio_certificat=0,
            total_consolidacio_hores=0,
            total_consolidacio_certificat=0,
            total_employment_insertions=0,
            total_constitutions=0,
        )
        for row in response.context_data['rows']:
            totals['total_members_h'] += row.members_h if row.members_h else 0
            totals['total_members_d'] += row.members_d if row.members_d else 0
            totals['total_members_total'] += row.members_total if row.members_total else 0
            totals['total_acollida_hores'] += row.acollida_hores if row.acollida_hores else 0
            totals['total_acollida_certificat'] += 1 if row.acollida_certificat else 0
            totals['total_proces_hores'] += row.proces_hores if row.proces_hores else 0
            totals['total_proces_certificat'] += 1 if row.proces_certificat else 0
            totals['total_constitucio_hores'] += row.constitucio_hores if row.constitucio_hores else 0
            totals['total_constitucio_certificat'] += 1 if row.constitucio_certificat else 0
            totals['total_consolidacio_hores'] += row.consolidacio_hores if row.consolidacio_hores else 0
            totals['total_consolidacio_certificat'] += 1 if row.consolidacio_certificat else 0
            totals['total_employment_insertions'] += \
                len(row.employment_insertions.all()) if row.employment_insertions else 0
            totals['total_constitutions'] += 1 if row.constitution_date else 0

        response.context_data['totals'] = totals

        return response

    # def has_change_permission(self, request, obj=None):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
