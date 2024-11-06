## Projet Django - Gestion de Projets
Ce projet permet de gérer des projets avec des informations telles que le titre, la description, l'état (complété ou non), et la date d'échéance. Vous pouvez également ajouter des tags à chaque projet.

## Installation
Clonez le repository :

```bash
git clone https://github.com/votreutilisateur/nom-du-projet.git
cd nom-du-projet
```
## Prérequis VERSION WINDOWS
- Python 3.12 ou plus récent
- Django 5.1 ou plus récent
  
Téléchargez pip :
```bash
python get-pip.py
```
Créez l'environnement virtuel et activez-le :

```bash
python -m venv venv
.\venv\Scripts\Activate
```
Installez toutes les dépendances :

```bash
pip install -r requirements.txt
```
## Prérequis VERSION LINUX
Créez un environnement virtuel :

```bash
python3 -m venv venv
```
Entrez dans l'environnement virtuel :

```bash
source venv/bin/activate
```
Puis, installez toutes les dépendances :

```bash
python -m ensurepip --upgrade
pip install -r requirements.txt
```
## Lancement
Le programme nécessite deux terminaux.

Dans le premier terminal, lancez le serveur Django :
```bash
py manage.py runserver
```
Dans le deuxième terminal, lancez le worker Celery :

```bash
celery -A djangotest worker -l info
```
Allez à http://127.0.0.1:8000/ pour accéder à votre projet !

Vous pouvez créer et modifier des projets.

Pour accéder au panneau administrateur : http://127.0.0.1:8000/admin/

## Commandes
Pour effectuer des tests :

```bash
py manage.py test
```
Pour appliquer les migrations :

```bash
py manage.py makemigrations
py manage.py migrate
```
