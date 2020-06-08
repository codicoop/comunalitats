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
            'members_h': Count('partners',
                               filter=Q(partners__gender='MALE')),
            'members_d': Count('partners',
                               filter=Q(partners__gender='FEMALE')),
            'members_total': Count('partners'),
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
        #
        # totals = dict(
        #     turns=0,
        #     total_to_pay=0,
        #     total_grants_obtained=0,
        #     total_to_pay_after_grants=0,
        #     total_payments_without_grants=0,
        #     to_pay=0
        # )
        # for row in response.context_data['rows']:
        #     totals['turns'] += row.turns if row.turns else 0
        #     totals['total_to_pay'] += row.total_to_pay if row.total_to_pay else 0
        #     totals['total_grants_obtained'] += row.total_grants_obtained if row.total_grants_obtained else 0
        #     totals['total_to_pay_after_grants'] += row.total_to_pay_after_grants if row.total_to_pay_after_grants else 0
        #     totals['total_payments_without_grants'] += row.total_payments_without_grants \
        #         if row.total_payments_without_grants else 0
        #     totals['to_pay'] += row.to_pay if row.to_pay else 0
        #
        # response.context_data['totals'] = totals

        return response

    # def has_change_permission(self, request, obj=None):
    #     return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
