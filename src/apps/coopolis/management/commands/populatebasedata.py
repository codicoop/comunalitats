# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/

from django.core.management.base import BaseCommand
from apps.coopolis.basedata import basedata_towns
from apps.coopolis.models import Town, User
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Populates the database with the basic information that it needs after a new installation.'

    def handle(self, *args, **options):

        """ The IDs migration was needed only for Coòpolis, to update the database from the
        original towns to the new one, generated using the Conveni spreadsheet towns list.
        After putting that in production, Coòpolis no longer needs this, nor any new
        installation.

        self.migrate_old_towns_ids()
        """

        """ The creation is very slow because is designed to merge the new towns data into
        a database that is already in use and with the old towns system.
        Although this is no longer needed because it's already applied to Coòpolis in 
        production, and new installations are going to be clean, it's harmless and not worth
        rewriting it at the moment."""
        self.create_towns()

    @staticmethod
    def create_towns():
        """ These 2 weird methods are because of the FK constraints in postgres.
        Given that we have to be able to run this script anywhere, and the ways
        to disable the constraints are dangerous and unreliable, I chose for this
        more compatible way.
        """
        new_towns = basedata_towns.towns()
        old_towns_obj = Town.objects.order_by('id')
        num_old_towns = len(old_towns_obj)  # 949
        num_new_towns = len(new_towns)  # 947
        cursor = 0
        if num_old_towns >= num_new_towns:
            for old_town in old_towns_obj:
                try:
                    print("Updating old town: '{}' with value: '{}'".format(old_town.name, new_towns[cursor]))
                    old_town.name = new_towns[cursor]
                    old_town.save()
                except IndexError:
                    print("Deleting old town {}".format(old_town.name))
                    old_town.delete()
                cursor += 1
            print("Finished populating towns by UPDATING+DELETING.")
        else:
            for new_town in new_towns:
                # Tb ha de fer els updates, però els que sobrin, s'han d'inserir.
                obj, created = Town.objects.update_or_create(
                    id=cursor, defaults={'name': new_town}
                )
                if created:
                    print("Created town: {}".format(new_town))
                else:
                    print("Updated town: {}".format(new_town))
                cursor += 1
            print("Finished populating towns by UPDATE OR CREATE.")

    @staticmethod
    def migrate_old_towns_ids():
        equivalences = basedata_towns.migration_id_equivalences()
        for town in equivalences:
            User.objects.filter(town=town['town_id']).update(town=town['new_id'])
            print("Updated users that had town id {} for the new town id: {}".format(town['town_id'], town['new_id']))
