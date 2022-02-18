from multiprocessing import context
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.db.models import Sum, Count, F
from users.models import Users


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
    project_list = []
    rate_list =[]
    projects = Project.objects.all()
    for project in projects:
        project_list.append(Images.objects.filter(project_id=project.project_id))
        rate_list.append(Rate.objects.filter(project_id=project.project_id))



    context = {'project_list': project_list,
               }
    return render(request, 'project/project_list.html', context)




# home 
def home(request):
   
    latestProjects = Project.objects.order_by('start_date')[0:5]
    latestProjectsList = []
    for project in latestProjects:
      
        latestProjectsList.append({
            'id': project.project_id,
            'title': project.title,
            'details': project.details,
            'target': project.total_target,
            'start_date': project.start_date,
        })
    
    categories = Categories.objects.all()
    context = {
        'latestProjectsList': latestProjectsList,
        'categories' :categories , 
    }
    return render(request, "home.html", context)

def project_list(request, id):
    project_list = []
    category_projects = Project.objects.filter(category_id=id).values(('project_id'))
    for project in category_projects:
        project_list.append(Images.objects.filter(project_id=project['id']))

    context = {'project_list': project_list}
    return render(request, 'list_projects.html', context )


def project_info(request, id):
    context = {}
    project_data = Project.objects.get(project_id=id)
    category_data = Categories.objects.get(category_id=project_data.category_id.category_id)
    images = Images.objects.filter(project_id=project_data.project_id)
    tags = Tags.objects.filter(project_id=project_data.project_id)
    rate = Rate.objects.filter(project_id=project_data.project_id)
    sum = 0
    count = 0
    for i in rate:
            sum += i.rate
            count += 1

    context['project'] = project_data
    context['category'] = category_data
    context['images'] = images[0]
    context['tags'] = tags
    context['sum'] = sum/count

    return render(request, 'project/project_info.html', context)



















