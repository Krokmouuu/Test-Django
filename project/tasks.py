from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from typing import Optional

# @shared_task 
# def mail_function(projet_id: int):
#     from .models import Project  # Import here to avoid circular imports
#     print(f"Envoi d'email pour projet ID {projet_id}")
#     try:
#         projet = Project.objects.get(id=projet_id)
#         sujet = f"Nouveau Projet Créé : {projet.title}"
#         message = f"Votre projet '{projet.title}' a été créé avec succès."
#         email_sender = settings.DEFAULT_FROM_EMAIL

#         print(email_sender)

#         if email_sender:
#             send_mail(sujet, message, email_sender, [email_sender])
#             return f"Email envoyé à {email_sender}."
#         else:
#             return "Pas d'email de destinataire fourni."
#     except Project.DoesNotExist:
#         return f"Projet avec ID {projet_id} introuvable."
