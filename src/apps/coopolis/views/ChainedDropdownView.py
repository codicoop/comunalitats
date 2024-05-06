from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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
    subsidy_period = request.GET.get("data")
    last_subsidy_period = SubsidyPeriod.objects.filter().first()
    selected_subsidy_period = SubsidyPeriod.objects.filter(name=subsidy_period).first()
    item_start = ServicesChoices.A
    item_end = ServicesChoices.E
    # !TODO: revisar
    if last_subsidy_period == selected_subsidy_period:
        item_start = ServicesChoices.F
        item_end = ServicesChoices.J
    if not selected_subsidy_period or subsidy_period == "Sense justificar":
        services = None
    elif subsidy_period:
        services = {
            item.value: item.label
            for item in ServicesChoices
            if item in range(item_start, item_end + 1)
        }
    return JsonResponse(data=services, safe=False)
