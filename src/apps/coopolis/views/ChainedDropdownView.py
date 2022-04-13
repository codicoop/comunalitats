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
