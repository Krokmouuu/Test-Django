from django.db import models
from typing import Optional
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .tasks import mail_function

class Project(models.Model):
    """ Model for Projects, Title limited to 255 characters, description, image and due date are optional, completed is a boolean field """
    title: str = models.CharField(max_length=255)
    description: Optional[str] = models.TextField(blank=True, null=True)
    image: Optional[models.ImageField] = models.ImageField(upload_to='djangotest/images/', blank=True, null=True)
    completed: bool = models.BooleanField(default=False)
    due_date: Optional[models.DateField] = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title
    
class Tag(models.Model):
    """ Model for Tags, title limited to 255 characters, projects is a many to many field """
    projects = models.ManyToManyField(Project)
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

# @receiver(post_save, sender=Project) # Signal sent after a project is created
# def signal_mail(sender, instance, created, **kwargs):
#     if created:
#         mail_function.delay(instance.id) # Send email with Celery