from csv import QUOTE_NONE, QUOTE_NONNUMERIC
from multiprocessing import context
from queue import Empty
from unicodedata import category
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect,reverse
from .models import *
from django.db.models import Sum, Count, F
from users.models import Users
from django.db.models import Q, Max, Min


#######################################
# create project
def create_project(request):
    context = {}
    if request.method == 'GET':
        categories = Categories.objects.all()
        context['catg'] = categories
        return render(request, 'project/create_project.html', context)
    elif request.method == 'POST':
        project_title = request.POST['project_title']
        project_details = request.POST['projectdetails']
        total_target = request.POST['totaltarget']
        category = Categories.objects.get(category_name=request.POST['category'])
        project_Start_date = request.POST['startdate']
        project_End_date = request.POST['enddate']
        images = request.FILES.getlist('projectimage[]')

        project = Project.objects.create(title=project_title, details=project_details, total_target=total_target,start_date=project_Start_date, end_date=project_End_date, category_id=category,user_id_id=request.session.get('id'))

        if images:
            for i in images:
                image = Images(img=i, project_id=project)
                image.save()

        for tag in request.POST["tags"].split(","):
            Tags(project_id=project, tag_name=tag).save()
        return redirect('list_project')
        #return render(request, 'project/project_list.html', context)


#######################################
# List Projects
def list_project(request):
    project_list = []
    rate_list = []
    projects = Project.objects.all()

    for project in projects:
        project_list.append(Images.objects.filter(project_id=project.project_id))
        rate_list.append(Rate.objects.filter(project_id=project.project_id))

    context = {'project_list': project_list,
               }
    return render(request, 'project/project_list.html', context)


# --------------------------------- HOME Page -----------------------------------------
def home(request):
    latestProjects = Project.objects.values('project_id').order_by('start_date')[0:5]
    FeaturedProjects = Project.objects.values('project_id')[0:5]
    topratedProjects = Rate.objects.values('project_id').annotate(rate=Max('rate')).order_by('-rate')[0:5]

    latestProjectsList = []

    for project in latestProjects:
        latestProjectsList.append(Images.objects.filter(project_id=project['project_id']))
    featuredProjectsList = []

    for project in FeaturedProjects:
        featuredProjectsList.append(Images.objects.filter(project_id=project['project_id']))
    topRatedProjectsList = []

    for project in topratedProjects:
        topRatedProjectsList.append(Images.objects.filter(project_id=project['project_id']))
    print(topRatedProjectsList)
    categories = Categories.objects.all()
    context = {
        'latestProjectsList': latestProjectsList,
        'categories': categories,
        'featuredProjectsList': featuredProjectsList,
        'topRatedProjectsList': topRatedProjectsList,
    }
    return render(request, "home.html", context)


# --------------------------------- List of Project in Category Page -----------------------------------------

def project_list(request, id):
    project_list = []
    category = Categories.objects.get(category_id=id)
    category_name = category.category_name
    category_projects = Project.objects.filter(category_id=id).values('project_id')
    for project in category_projects:
        project_list.append(Images.objects.filter(project_id=project['project_id']))

    context = {'project_list': project_list,
               'category_name': category_name
               }
    print(project_list)
    return render(request, 'list_projects.html', context)


def project_info(request, id):
    context = {}
    project_data = Project.objects.get(project_id=id)
    category_data = Categories.objects.get(category_id=project_data.category_id.category_id)
    images = Images.objects.filter(project_id=project_data.project_id)
    tags = Tags.objects.filter(project_id=project_data.project_id)
    rate = Rate.objects.filter(project_id=project_data.project_id)
    donation = Donation.objects.filter(project_id=project_data.project_id)
    sum = 0
    count = 0
    counter = 0
    project_list = []
    projects = Project.objects.all()
    print(images)

    for project in projects:
        project_list.append(Images.objects.filter(project_id=project.project_id))
        # counter += 1
    print(project_list)

    for i in rate:
        sum += i.rate
        count += 1

    context['project'] = project_data
    context['category'] = category_data
    context['images'] = images
    context['tags'] = tags
    context['sum'] = sum
    context['count'] = count
    context['donation'] = donation
    context['project_list'] = project_list

    # percentage = (donation[0].donation_value/project_data.total_target)*100


    if request.method == 'GET':
        return render(request, 'project/project_info.html', context)
    elif request.method == 'POST':
        if not donation:
            Donation.objects.create(project_id=project_data, donation_value=request.POST['value'], user_id_id=request.session.get('id'))
            return render(request, 'project/project_info.html', context)

        else:
            Donation.objects.filter(project_id=project_data, user_id_id=request.session.get('id')).update(
                donation_value=F("donation_value") + request.POST.get("value"))

        return redirect(f'/project/project_info/{project_data.project_id}')





    return render(request, 'project/project_info.html', context)


def add_comment(request, id):
    project = Project.objects.get(project_id=id)
    comments = Comment.objects.filter(project_id=project.project_id)
    user = request.session.get('id')

    context = {}
    context['project'] = project
    context['comments'] = comments
    context['user'] = user
    if request.method == "GET":
        return render(request, 'project/hi.html', context)

    elif request.method == "POST":
        Comment.objects.create(project_id=project, comment=request.POST['comment'], user_id_id=request.session.get('id'))

        return render(request, 'project/hi.html', context)


def cancel_project(request, id):
    if request.method == 'GET':
        return render(request, 'project/cancel.html')

    if request.method == 'POST':
        project = Project.objects.get(project_id=id)
        Project.objects.filter(project_id=project.project_id).delete()

        return HttpResponseRedirect('/project/project_list')


def report_project(request, id):
    context={}
    context['id'] = id
    project = Project.objects.get(project_id=id)

    if request.method == 'GET':
        return render(request, 'project/report_project.html', context)

    elif request.method == 'POST':
        ProjectReports.objects.create(project_id_id=project.project_id, message='this project', user_id_id=request.session.get('id'))

    return redirect(f'/project/project_info/{project.project_id}')


def report_comment(request, id):
    comments = Comment.objects.filter(comment_id=id)
    project = Comment.objects.filter(project_id=comments[0].project_id)

    if request.method == 'GET':
        return render(request, 'project/report_comment.html')
    if request.method == 'POST':
        # project = Project.objects.get(project_id=id)
        context = {}
        # context['project'] = project
        context['comments'] = comments
        comment = Comment.objects.get(comment_id=id)
        CommentReports.objects.create(comment_id_id=comment.comment_id, user_id_id=request.session.get('id'))
        # return render(request,'project/hi.html', context)
        return redirect(f'/project/comments/{project[0].project_id.project_id}')
# def image_slider(request):
#     project_list = []
#     rate_list =[]
#     projects = Project.objects.all()
#
#     for project in projects:
#         project_list.append(Images.objects.filter(project_id=project.project_id))
#         rate_list.append(Rate.objects.filter(project_id=project.project_id))
#
#     context = {'project_list': project_list,
#                }
#     print(project_list)
#     return render(request, 'project/project_info.html', context)





# --------------------------------- Search Function-----------------------------------------
# we use Q objects to make more complex queries following
# Use | (OR) operator to search for only one field. For example, when searching title | content, both don’t have to be true, only one is okay, when searching for a word such as “python”, so it(python) doesn’t have to be contained in both title and content fields
# https://stackpython.medium.com/django-search-with-q-objects-tutorial-9c701db74e0e
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
