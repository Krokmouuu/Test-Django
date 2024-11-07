from django.core.management.base import BaseCommand, CommandError
from project.models import Project, Tag
import os
import shutil

class Command(BaseCommand):
    help = 'Supprime tous les projets'

    def handle(self, *args, **kwargs):
        confirmation = input("Êtes-vous sûr de vouloir supprimer tous les projets ? (oui/non): ")
        if confirmation.lower() == "oui":
            count, _ = Project.objects.all().delete()
            if os.path.exists('djangotest/images/'):
                shutil.rmtree('djangotest/images/')
            Tag.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'{count} projets ont été supprimés avec succès.'))
        else:
            self.stdout.write(self.style.WARNING('Action annulée. Aucun projet n\'a été supprimé.'))
