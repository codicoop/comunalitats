from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime

from apps.coopolis.choices import ServicesChoices
from apps.projects.models import SubsidyPeriod


@login_required
def get_sub_services(request):
    service = int(request.GET.get("data")) if request.GET.get("data") else None
    sub_services = {}
    try:
        service = ServicesChoices(service)
    except ValueError:
        pass
    else:
        sub_services = {item.value: item.label for item in service.get_sub_services()}
    return JsonResponse(data=sub_services, safe=False)


@login_required
def get_subsidy_period(request):
    """
    Maig de 2024:
    Hi ha canvis a Serveis i Subserveis que impliquen que els items de la
    convocatòria 2024-2026 han de tenir unes opcions diferents dels de la
    convocatòria 2022-2024.

    S'ha resolt afegint les opcions als ServicesChoices i SubServicesChoices,
    i al "front" (admin) s'ha implementat un JS que mostra unes opcions o altres
    segons la convocatòria seleccionada.

    Per això es fa aquest sistema de definir el rang que ha de retornar amb
    item_start i item_end.

    EN CAS QUE S'HAGI DE SEGUIR AFEGINT OPCIONS DIFERENTS EN NOVES
    CONVOCATÒRIES:
    Crec que caldrà migrar cap a un sistema de models en el que servei i
    subservei pengin de Convocatòria.
    """

    subsidy_period = None
    start_date = request.GET.get("data")
    if start_date:
        try:
            date_start = datetime.strptime(start_date, "%d/%m/%Y").date()
        except ValueError:
            return JsonResponse(
                data=None,
                safe=False,
            )
        try:
            subsidy_period = SubsidyPeriod.objects.get(date_start__lte=date_start, date_end__gte=date_start)
        except SubsidyPeriod.DoesNotExist:
            return JsonResponse(
                data=None,
                safe=False,
            )
    selected_subsidy_period = request.GET.get("selected_subsidy_period")
    if selected_subsidy_period:
        try:
            subsidy_period = SubsidyPeriod.objects.get(id=selected_subsidy_period)
        except SubsidyPeriod.DoesNotExist:
            return JsonResponse(
                data=None,
                safe=False,
            )

    if not subsidy_period:
        # Could reach it if none of the GET parameters are present
        return JsonResponse(
            data=None,
            safe=False,
        )

    services = ServicesChoices.get_services_for_subsidy_period_name(
        subsidy_period.name,
    )
    return JsonResponse(data=services, safe=False)
