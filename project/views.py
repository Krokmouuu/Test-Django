from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.

def create(request: HttpRequest):
    
    return HttpResponse('create')

def update(request: HttpRequest, project_id : int):
    return HttpResponse('update')

def get(request: HttpRequest, project_id: int):
    return HttpResponse('get')

def get_all(request: HttpRequest):
    return HttpResponse('get all')

def delete(request: HttpRequest, project_id: int):
    return HttpResponse('delete')