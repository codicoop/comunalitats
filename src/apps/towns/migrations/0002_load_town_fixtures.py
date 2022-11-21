from django.conf import settings
from django.core.management import call_command
from django.db import migrations


def load_fixtures(apps, schema_editor):
    print("\nLoading Towns")
    path = settings.BASE_DIR + "/apps/towns/fixtures/towns.json"
    call_command("loaddata", path, verbosity=2)
    print("Towns loaded.")


class Migration(migrations.Migration):

    dependencies = [
        ("towns", "0001_initial"),
    ]

    operations = [migrations.RunPython(load_fixtures)]
