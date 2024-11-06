# Projet Django - Gestion de Projets

Ce projet permet de gérer des projets avec des informations telles que le titre, la description, l'état (complété ou non), et la date d'échéance. Vous pouvez également ajouter des tags à chaque projet.

## Prérequis

- Python 3.12 ou plus récent
- Django 5.1 ou plus récent
- Redis .........

## Installation

 Clonez le repository :
   ```bash
   git clone https://github.com/votreutilisateur/nom-du-projet.git
   cd nom-du-projet
```

## Lancement

```bash 
py manage.py runserver
celery -A nom-du_-rojet worker -l info
redis .....
```
Aller a http://127.0.0.1:8000/

Vous etes sur le projet !
Vous pouvez creer des projets et les modifier,

Pour acceder au panel administrateur : http://127.0.0.1:8000/admin/

## Commandes

Pour effectuer des tests 
```bash
py manage.py test
```

Pour appliquer les migrations
```bash
py manage.py makemigrations
py manage.py migrate
```
