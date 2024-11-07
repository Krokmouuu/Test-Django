from django.test import TestCase, Client
from ..models import Project, Tag
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.core.exceptions import ValidationError
import time

class ProjectUrlTest(TestCase):
    """Tester les vues de l'application projet."""
    def setUp(self):
        """Préparer les données et le client de test."""
        self.client = Client() # Creating instance of the Client to simulate HTTP requests
        self.project_data = { # Data for the project
            'title': 'Test Project',
            'description': 'A description for the test project',
            'completed': False,
            'due_date': timezone.now().date() + timedelta(days=7)
        }
        self.project = Project.objects.create(**self.project_data) # Create a project in the database
        self.main_page = reverse('main_page')
        self.list_url = reverse('retrieve_all_project') 
        self.detail_url = reverse('retrieve_project', args=[self.project.id])
        self.create_url = reverse('create_project')
        self.update_url = reverse('update_project', args=[self.project.id])
        self.delete_url = reverse('delete_project', args=[self.project.id])

    def test_main_page(self):
        """Tester la page d'accueil."""
        response = self.client.get(self.main_page)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_page.html')
        self.assertContains(response, f'<a href="{self.create_url}">Créer un Projet</a>')
        self.assertContains(response, f'<a href="{self.list_url}">Liste des Projets</a>')


    def test_project_list_view(self):
        """Tester la vue de liste des projets."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_projects.html')
        self.assertContains(response, f'<a href="{reverse("retrieve_project", kwargs={"project_id": self.project.id})}">Voir</a>')
        self.assertContains(response, f'<a href="{reverse("update_project", kwargs={"project_id": self.project.id})}">Éditer</a>')
        self.assertContains(response, f'<a href="{reverse("delete_project", kwargs={"project_id": self.project.id})}">Supprimer</a>')

    def test_project_detail_view(self):
        """Tester la vue détaillée d'un projet."""
        response = self.client.get(self.detail_url)
        url = reverse('retrieve_project', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'retrieve_project.html')
        self.assertContains(response, 'Test Project')
    
    def test_create_project_view(self):
        """Tester la vue de création d'un projet."""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_project.html')
        self.assertContains(response, '<input type="submit" value="Créer le Projet">')
        self.assertContains(response, '<button type="button" onclick="window.location.href=\'/\'">Retour</button>') # Check if the button is present with the correct return URL

    def test_update_project_view(self):
        """Tester la vue de mise à jour d'un projet."""
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_project.html')
        self.assertContains(response, '<button type="submit">Mettre à jour le projet</button>')
        self.assertContains(response, '<button type="button" onclick="window.location.href=\'/project/\'">Annuler</button>')

class ProjectFilterViewTest(TestCase):
    def setUp(self):
        """Préparer les données et le client de test."""
        self.client = Client()
        self.project_data1 = {
            'title': 'Project 1',
            'description': 'Test project 1',
            'completed': False,
            'due_date': timezone.now().date() + timedelta(days=7)
        }
        self.project_data2 = {
            'title': 'Project 2',
            'description': 'Test project 2',
            'completed': True,
            'due_date': timezone.now().date() + timedelta(days=10)
        }
        self.project1 = Project.objects.create(**self.project_data1)
        self.project2 = Project.objects.create(**self.project_data2)
        
        self.list_url = reverse('retrieve_all_project')
    
    def test_project_list_filter_by_completed(self):
        """Test du filtrage des projets par statut 'complété'."""
        response = self.client.get(self.list_url, {'completed': True})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Project 2')
        self.assertNotContains(response, 'Project 1')

    def test_project_list_filter_by_date(self):
        """Test du filtrage des projets par date."""
        response = self.client.get(self.list_url, {'due_date': str(self.project1.due_date)})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Project 1')
        self.assertNotContains(response, 'Project 2')