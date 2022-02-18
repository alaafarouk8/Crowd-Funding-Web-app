from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, HttpResponse
from .models import *

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



# home 
def home(request):
   
    latestProjects = Project.objects.order_by('start_date')[:5]

    # preparing Latest Projects in One List
    latestProjectsList = []
    for project in latestProjects:
      
        latestProjectsList.append({
            'id': project.project_id,
            'title': project.title,
            'details': project.details,
            'target': project.total_target,
            'start_date': project.start_date,
        })

    context = {
        'latestProjectsList': latestProjectsList,
    }
    return render(request, "home.html", context)


