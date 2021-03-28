import operator

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
from accounts.models import Project
from init_test.models import student_score
from subjects.models import suggested_subject, subject


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('register')
        elif first_name == '' or email == '' or password == '' or username == '':
            messages.info(request, 'Re-enter Details')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('register')

        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                            last_name=last_name)
            user.save()
            print('user created')
            return redirect('login')
    elif request.method == 'GET':
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        password = request.POST['password']
        username = request.POST['username']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')

    else:

        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def dashboard(request):
    user_id = request.user.id
    if suggested_subject.objects.filter(student_id=user_id).exists():
        global_map = {}
        student_data = student_score.objects.filter(student_id=user_id).values()[0]
        del student_data['id']
        del student_data['student_id']

        for ele in list(student_data):
            if student_data[ele] == False:
                student_data.pop(ele)

        n = len(subject.objects.values())
        for i in range(1, n + 1):
            subject_data = subject.objects.filter(id=i).values()[0]
            del subject_data['id']
            del subject_data['subject_name']

            all_keys = list(student_data.keys())

            counter1 = 0

            for ele in all_keys:
                if subject_data[ele]:
                    counter1 += 1

            global_map[subject.objects.filter(id=i).values()[0]['subject_name']] = counter1

        global_map = dict(sorted(global_map.items(), key=operator.itemgetter(1)))
        global_arr = list(global_map.keys())
        global_arr.reverse()

        return render(request, 'dashboard.html', {'subject': global_arr[:4]})
    else:
        return render(request, 'dashboard.html')


def submitproject(request):
    user_id = request.user.id
    if request.method == "POST":
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')
        role = ''
        if request.POST.get('your_role') == '1':
            role = "Programmer/Developer"
        elif request.POST.get('your_role') == '2':
            role = "Content Creator"
        elif request.POST.get('your_role') == '3':
            role = "Hardware"
        elif request.POST.get('your_role') == '4':
            role = "Team Leader"
        else:
            role = "Resource Manager"

        skills = ['', '', '', '', '']
        if request.POST.get('prof1'):
            skills[0] = request.POST.get('prof1')
        if request.POST.get('field2'):
            skills[1] = request.POST.get('field2')
        if request.POST.get('field3'):
            skills[2] = request.POST.get('field3')
        if request.POST.get('field4'):
            skills[3] = request.POST.get('field4')
        if request.POST.get('field5'):
            skills[4] = request.POST.get('field5')

            projects = Project.objects.create(student_id=user_id, project_name=project_name,
                                              project_description=project_description, project_role=role,
                                              skills_used1=skills[0], skills_used2=skills[1], skills_used3=skills[2],
                                              skills_used4=skills[3], skills_used5=skills[4])
            projects.save()

        return redirect('dashboard')
