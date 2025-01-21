# Generated by Django 3.2.14 on 2024-08-02 07:08

from django.db import migrations

from apps.coopolis.choices import ServicesChoices


def migrate_service_2024(apps, schema_editor):
    activity_model = apps.get_model("cc_courses", "Activity")
    convocatoria_model = apps.get_model("dataexports", "SubsidyPeriod")
    try:
        convocatoria_2024 = convocatoria_model.objects.get(
            date_start__year=2024,
            date_end__year=2025,
        )
    except convocatoria_model.DoesNotExist:
        print("Els Serveis no s'han pogut migrar als de 2024 degut a que la "
              "convocatòria 2024-2025 no existeix.")
        return
    date_range = convocatoria_2024.date_start, convocatoria_2024.date_end
    activities = activity_model.objects.filter(
        date_start__range=date_range,
        service__isnull=False,
    )
    for activity in activities:
        if 10 <= activity.service <= 50:
            service_2024 = get_equivalent_service(activity.service)
            print(f"Activity {activity.name} has {activity.service}, replacing "
                  f"it with {service_2024}")
            activity.service = service_2024
            # If the service is not valid for the convocatòria, the sub service
            # will not be either, but we cannot deduce the new subservice
            # because they completely changed in number and order.
            activity.sub_service = None
            activity.save()
        else:
            print(f"Activity {activity.name} has {activity.service}. Nothing to"
                  " replace.")


class Migration(migrations.Migration):

    dependencies = [
        ('dataexports', '0001_initial'),
        ('cc_courses', '0008_auto_20240719_1559'),
    ]

    operations = [
        migrations.RunPython(migrate_service_2024),
    ]


def get_equivalent_service(service):
    """
    In ServicesChoices, the options A to E are the old ones and the ones from
    F to K the new ones.
    The old service "A" value is 10, and the corresponding new service "A" is
    60, and the same relation goes for each of them.
    """
    return service + 50
