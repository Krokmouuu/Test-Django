from django.test import TestCase, Client
from ..models import Project, Tag
from django.utils import timezone
from django.urls import reverse

class ProjectModelTest(TestCase):
    
    def setUp(self):
        """Préparer un projet de base pour les tests."""
        self.project_data = {
            'title': 'Test Project',
            'description': 'A description for the test project',
            'completed': False,
            'due_date': timezone.now().date() + timezone.timedelta(days=7)
        }
        
    def test_create_project(self):
        """Tester la création d'un projet."""
        url = reverse('create_project')
        response = self.client.post(url, self.project_data)
        self.assertEqual(Project.objects.count(), 1)
        self.assertTemplateUsed(response, 'success.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<button onclick="window.location.href=\'/create/\'">Créer un autre projet</button>')
        self.assertContains(response, '<button onclick="window.location.href=\'/\'">Retour à l\'accueil</button>')
        self.assertTrue(Project.objects.filter(title='Test Project').exists())


    def test_read_project(self):
        """Tester la lecture d'un projet."""
        project = Project.objects.create(**self.project_data)
        retrieved_project = Project.objects.get(id=project.id)
        self.assertEqual(retrieved_project.title, 'Test Project')

    def test_update_project(self):
        """Tester la mise à jour d'un projet."""
        project = Project.objects.create(**self.project_data)
        updated_data = {
            'title': 'Updated Project Title',
            'completed': True,
            'due_date': timezone.now().date() + timezone.timedelta(days=5)
        }
        response = self.client.post(reverse('update_project', args=[project.id]), updated_data)
        self.assertEqual(response.status_code, 302)
        updated_project = Project.objects.get(id=project.id)
        self.assertEqual(updated_project.title, updated_data['title'])
        self.assertTrue(updated_project.completed)
        self.assertEqual(updated_project.due_date, updated_data['due_date'])

    def test_delete_project(self):
    
        """Tester la suppression d'un projet."""
        project = Project.objects.create(**self.project_data)
        project_id = project.id
        response = self.client.get(reverse('delete_project', args=[project.id]))
        self.assertContains(response, '<button type="submit">Confirmer la suppression</button>')
        self.assertContains(response, '<a href="/project/">Annuler</a>')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('delete_project', args=[project.id]))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Project.DoesNotExist):
            Project.objects.get(id=project_id)

class TagModelTest(TestCase):

    def setUp(self):
        """Préparer des données de test pour les tags."""
        self.project = Project.objects.create(
            title='Test Project for Tag',
            description='Description for the tag test',
            completed=False
        )
        self.tag_data = {'title': 'Test Tag'}

    def test_create_tag(self):
        """Tester la création d'un tag."""
        tag = Tag.objects.create(**self.tag_data)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(tag.title, 'Test Tag')

    def test_add_tag_to_project(self):
        """Tester l'ajout d'un tag à un projet."""
        tag = Tag.objects.create(**self.tag_data)
        tag.projects.add(self.project)
        self.assertEqual(tag.projects.count(), 1)
        self.assertEqual(self.project.tag_set.count(), 1)
        self.assertTrue(self.project.tag_set.filter(title='Test Tag').exists())

    def test_remove_tag_from_project(self):
        """Tester la suppression d'un tag d'un projet."""
        tag = Tag.objects.create(**self.tag_data)
        tag.projects.add(self.project)
        tag.projects.remove(self.project)
        self.assertEqual(tag.projects.count(), 0)
        self.assertEqual(self.project.tag_set.count(), 0)