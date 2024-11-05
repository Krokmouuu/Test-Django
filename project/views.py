from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from .models import Project, Tag
from .serializers import ProjectSerializer, TagSerializer
from django.http import HttpResponse, HttpRequest

@api_view(['POST', 'GET'])
def main_page(request: HttpRequest):
    return render(request, 'main_page.html')
    
def create(request: HttpRequest):
    if request.method == 'POST':
        data = request.POST.copy()
        data['image'] = request.FILES.get('image')
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            project = serializer.save()
            tags_list = request.POST.get('tags', '')
            if tags_list:
                tags_list = [tag.strip() for tag in tags_list.split(',')]
                for tag in tags_list:
                    tag, created = Tag.objects.get_or_create(title=tag) 
                    tag.projects.add(project)
            return render(request, 'success.html')
        else:
            return render(request, 'create.html', {'serializer': serializer})
    return render(request, 'create.html')


def update(request: HttpRequest, project_id : int):
    return HttpResponse('update')

def get(request: HttpRequest, project_id: int):
    return HttpResponse('get')

def get_all(request: HttpRequest):
    if request.method == 'GET':
        projects = Project.objects.all()
        completed_filter = request.GET.get('completed')
    if completed_filter:
        if completed_filter == 'True':
            projects = projects.filter(completed=True)
        elif completed_filter == 'False':
            projects = projects.filter(completed=False)
    due_date_filter = request.GET.get('due_date') 
    if due_date_filter:
        projects = projects.filter(due_date=due_date_filter)
        projects = sorted(projects, key=lambda p: p.due_date or '', reverse=False)
    return render(request, 'list_projects.html', {'projects': projects})

def delete(request: HttpRequest, project_id: int):
    return HttpResponse('delete')