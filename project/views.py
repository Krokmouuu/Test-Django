from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Project, Tag
from .serializers import ProjectSerializer
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from djangotest.throttling import CreateThrottle

def handle_error(message, status_code=400): # 400 is the default status code
    return HttpResponse(message, status=status_code)

@api_view(['POST', 'GET']) # This is a decorator that allows us to use the function as an API endpoint
def main_page(request: HttpRequest): # Main page view
    return render(request, 'main_page.html')
def create(request: HttpRequest):

    throttle = CreateThrottle() # Create an instance of the throttle class
    if not throttle.allow_request(request, None): # Check if the request is allowed
        return handle_error('Trop de requêtes. Veuillez réessayer plus tard.', 429) # Return an error if the request is not allowed
    if request.method == 'POST':
        data = request.POST.copy() 
        data['image'] = request.FILES.get('image') # Get image from request

        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            project = serializer.save()
            tags_list = request.POST.get('tags', '').rstrip(',').split(',') # Split tags
            tags_list = [tag.strip() for tag in tags_list if tag.strip()] # Remove empty tags

            for tag in tags_list:
                tag = tag.strip()
                tag_obj, created = Tag.objects.get_or_create(title=tag) # Get or create tag
                tag_obj.projects.add(project) 

            return render(request, 'success.html')
    elif request.method == 'GET':
        return render(request, 'create_project.html')
    return handle_error('Méthode non autorisée', 405)
        
def update(request: HttpRequest, project_id: int):
    project = get_object_or_404(Project, id=project_id) # Get project by ID

    if request.method == 'GET':
        return render(request, 'update_project.html', {'project': project,})

    elif request.method == 'POST':
        data = request.POST.copy()

        if 'image' in request.FILES: # Check if image is in request
            data['image'] = request.FILES.get('image')
            serializer = ProjectSerializer(project, data=data)
        else: # If not, use the image from the project
            data['image'] = project.image
            serializer = ProjectSerializer(project, data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect('retrieve_all_project')
        else:
            return render(request, 'update_project.html', {
                'project': project,
                'errors': serializer.errors
            })

    return handle_error('Méthode non autorisée', 405)

def get(request: HttpRequest, project_id: int):
    project = get_object_or_404(Project, id=project_id)
    print(project)

    if request.method == 'GET':
        tags = Tag.objects.filter(projects=project)
        return render(request, 'retrieve_project.html', {'project': project, 'tags': tags})

    return handle_error('Méthode non autorisée', 405)

def get_all(request: HttpRequest):
   if request.method == 'GET':
        projects = Project.objects.prefetch_related('tag_set') # Get all projects with tags
        completed_filter = request.GET.get('completed') # Get completed filter
        if completed_filter:
            if completed_filter == 'True':
                projects = projects.filter(completed=True)
            elif completed_filter == 'False':
                projects = projects.filter(completed=False)
        due_date_filter = request.GET.get('due_date') 
        if due_date_filter:
            projects = projects.filter(due_date=due_date_filter)
            projects = sorted(projects, key=lambda p: p.due_date or '', reverse=False) # Sort by due date
        return render(request, 'list_projects.html', {'projects': projects})
   else:
        return handle_error('Méthode non autorisée', 405)

def delete(request: HttpRequest, project_id: int):
    project = get_object_or_404(Project, id=project_id)
    if project is None:
        return handle_error('Projet introuvable', 404)
    if request.method == 'GET':
        return render(request, 'delete_project.html', {'project': project})
    elif request.method == 'POST':
        if project.image:
            if default_storage.exists(project.image.name):
                default_storage.delete(project.image.name)
        project.delete()
        Tag.objects.filter(projects__isnull=True).delete() # Delete tags with no projects
        return redirect('retrieve_all_project')

    return handle_error('Méthode non autorisée', 405)
