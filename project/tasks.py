from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task 
def mail_function(project_id: int):
    from .models import Project  # Import inside the function to avoid circular imports
    try:
        project = Project.objects.get(id=project_id)
        sujet = f"Nouveau Projet Créé : {project.title}"
        message = f"Votre projet '{project.title}' a été créé avec succès."
        email_sender = settings.DEFAULT_FROM_EMAIL

        print(f"Email Sender: {email_sender}")

        if email_sender:
            send_mail(sujet, message, email_sender, [email_sender])
            return f"Email envoyé à {email_sender}."
        else:
            return "Pas d'email de destinataire fourni."
    except Project.DoesNotExist:
        return f"Projet avec ID {project_id} introuvable."