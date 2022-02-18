from csv import QUOTE_NONE, QUOTE_NONNUMERIC
from multiprocessing import context
from queue import Empty
from unicodedata import category
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.db.models import Q  


#######################################
# create project
def create_project(request):
    context = {}
    if request.method == 'GET':
        categories = Categories.objects.all()
        context['catg'] = categories
        return render(request, 'project/create_project.html', context)
    elif request.method == 'POST':
        project_title = request.POST['title']
        project_details = request.POST['projectdetails']
        total_target = request.POST['totaltarget']
        category = Categories.objects.get(category_name=request.POST['category'])
        project_Start_date = request.POST['startdate']
        project_End_date = request.POST['enddate']
        images = request.FILES.getlist('projectimage[]')

        project = Project.objects.create(title=project_title, details=project_details, total_target=total_target,
                          start_date=project_Start_date, end_date=project_End_date, category_id=category)

        if images:
            for i in images:
                image = Images(img=i, project_id=project)
                image.save()

        for tag in request.POST["tags"].split(","):
            Tags(project_id=project, tag_name=tag).save()

        return render(request, 'project/hi.html', context)

#######################################
#List Projects
def list_project(request):
    projects = Project.objects.all()
    images = Images.objects.all()

    imgs = []
    for project in projects:
        img = Images.objects.filter(project_id=project.project_id)
        imgs.append(img)
    print(len(imgs))
    context = {}
    context['projects'] = projects
    context['images'] = imgs

    return render(request, 'project/project_list.html', context)


# --------------------------------- HOME Page -----------------------------------------
def home(request):
   
    latestProjects = Project.objects.values('project_id').order_by('start_date')[0:5]
    FeaturedProjects = Project.objects.values('project_id')[0:5]
    latestProjectsList = []
    for project in latestProjects:
        latestProjectsList.append(Images.objects.filter(project_id=project['project_id']))
    featuredProjectsList = []
    for project in FeaturedProjects:
        featuredProjectsList.append(Images.objects.filter(project_id=project['project_id']))

    print(latestProjectsList)
    categories = Categories.objects.all()
    context = {
        'latestProjectsList': latestProjectsList,
        'categories' :categories , 
        'featuredProjectsList':featuredProjectsList,
    }
    return render(request, "home.html", context)

# --------------------------------- List of Project in Category Page -----------------------------------------

def project_list(request, id):
    project_list = []
    category = Categories.objects.get(category_id=id)
    category_name=category.category_name
    category_projects = Project.objects.filter(category_id=id).values('project_id')
    for project in category_projects:
        project_list.append(Images.objects.filter(project_id=project['project_id']))
    
    context = {'project_list': project_list ,
               'category_name' :category_name
    }
    print(project_list)
    return render(request, 'list_projects.html',context )

# --------------------------------- Search Function-----------------------------------------
# we use Q objects to make more complex queries following
# Use | (OR) operator to search for only one field. For example, when searching title | content, both don’t have to be true, only one is okay, when searching for a word such as “python”, so it(python) doesn’t have to be contained in both title and content fields
#https://stackpython.medium.com/django-search-with-q-objects-tutorial-9c701db74e0e
def search(request):
    project_list = []
    if request.method == 'POST':
        query = request.POST.get('query')
        if query is not None:
            search = Q(title__icontains=query) | Q(tags__tag_name__icontains=query)
            results = Project.objects.filter(search).values('project_id')
            for project in results:
                project_list.append(Images.objects.filter(project_id=project['project_id']))
            
            return render(request, 'search_project.html', {'project_list': project_list})

        else:
            return render(request, 'search_project.html')
    else:
        return render(request, 'home.html')


