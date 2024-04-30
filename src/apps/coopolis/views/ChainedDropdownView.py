from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from apps.coopolis.choices import ServicesChoices


@login_required
def get_sub_services(request):
    service = int(request.GET.get("service")) if request.GET.get("service") else None
    sub_services = {}
    try:
        service = ServicesChoices(service)
    except ValueError:
        pass
    else:
        sub_services = {
            item.value: item.label for item in service.get_sub_services()
        }
    return JsonResponse(data=sub_services, safe=False)


@login_required
def get_subsidy_period(request):
    subsidy_period = request.GET.get("subsidy_period")
    item_start = ServicesChoices.A
    item_end = ServicesChoices.E
    # !TODO: revisar
    if subsidy_period == "1":
        item_start = ServicesChoices.F
        item_end = ServicesChoices.J

    if not subsidy_period:
        services = None
    elif subsidy_period:
        services = {
            item.value: item.label
            for item in ServicesChoices
            if item in range(item_start, item_end + 1)
        }
    return JsonResponse(data=services, safe=False)
