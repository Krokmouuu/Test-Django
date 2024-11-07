from django.test import TestCase, Client
from ..models import Project, Tag
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse

class ProjectViewsTest(TestCase):
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
        self.list_url = reverse('retrieve_all_project') 
        self.main_page = reverse('main_page')
        self.detail_url = reverse('retrieve_project', args=[self.project.id])
        self.create_url = reverse('create_project')
        self.update_url = reverse('update_project', args=[self.project.id])
        self.delete_url = reverse('delete_project', args=[self.project.id])

    def test_main_page_view(self):
        """Tester que la vue de la page principale fonctionne."""
        response = self.client.get(self.main_page) # Simulate a GET request to the URL
        self.assertEqual(response.status_code, 200) # Check if the response is successful
        self.assertTemplateUsed(response, 'main_page.html') # Check if the correct template is used
        
    def test_project_list_view(self):
        """Tester que la vue liste des projets fonctionne et affiche les projets."""
        response = self.client.get(self.list_url) # Simulate a GET request to the URL
        self.assertEqual(response.status_code, 200) # Check if the response is successful
        self.assertTemplateUsed(response, 'list_projects.html') # Check if the correct template is used
        self.assertContains(response, 'Test Project')  # Check if the project is in the response

    def test_project_detail_view(self):
        """Tester que la vue détail du projet fonctionne."""
        response = self.client.get(self.detail_url) # Simulate a GET request to the URL
        self.assertEqual(response.status_code, 200) # Check if the response is successful
        print(self.assertEqual(response.status_code, 200))
        self.assertTemplateUsed(response, 'retrieve_project.html') # Check if the correct template is used 
        self.assertContains(response, 'A description for the test project') # Check if the project description is in the response

    def test_project_create_view(self):
        """Tester la création d'un nouveau projet."""
        new_project_data = {
            'title': 'New Project',
            'description': 'Description of the new project',
            'completed': False,
            'due_date': timezone.now().date() + timedelta(days=10)
        }
        response = self.client.post(self.create_url, new_project_data) # Simulate a POST request
        self.assertEqual(Project.objects.count(), 2)  # Check if the project was created and added to the database

    def test_project_update_view(self):
        """Tester la mise à jour d'un projet existant."""
        updated_data = {
            'title': 'Updated Project',
            'description': 'Updated description',
            'completed': True,
            'due_date': timezone.now().date() + timedelta(days=5)
        }
        response = self.client.post(self.update_url, updated_data) # Simulate a POST request
        self.assertEqual(response.status_code, 302)  # Redirect after update
        self.project.refresh_from_db()  # Refresh the project instance from the database
        self.assertEqual(self.project.title, 'Updated Project') # Check if the project title was updated
        self.assertTrue(self.project.completed) # Check if the project is marked as completed

    def test_project_delete_view(self):
        """Tester la suppression d'un projet."""
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect after delete
        self.assertEqual(Project.objects.count(), 0)  # Check if the project was deleted from the database


