import operator

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
from accounts.forms import FeedbackForm
from accounts.models import feedback
from projects.models import Project
from init_test.models import student_score
from student.models import Student_Report
from subjects.models import suggested_subject, subject


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['pass']
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

        if Student_Report.objects.filter(student_id=user_id).exists():
            all_data = Student_Report.objects.filter(student_id=user_id).values().get()
            all_subjects_scores = all_data['subject_marks']
            # import pdb
            # pdb.set_trace()
            temp_sub = {}
            list_data = list(all_data['subject_marks'].keys())
            for i in list_data:
                temp_sub.update(all_subjects_scores[i])
            return render(request, 'dashboard.html', {'subject': global_arr[:4], 'subject_scores': temp_sub})
        else:
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
            # import pdb
            # pdb.set_trace()

        projects = Project.objects.create(student_id=user_id, project_name=project_name,
                                          project_description=project_description, project_role=role,
                                          skills_used1=skills[0], skills_used2=skills[1], skills_used3=skills[2],
                                          skills_used4=skills[3], skills_used5=skills[4])
        projects.save()

        return redirect('dashboard')


def feed(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # import pdb
            # pdb.set_trace()
            name = request.POST.get('name')
            rating = int(request.POST.get('rating'))
            comment = request.POST.get('comment')
            feedbacks = feedback.objects.create(name=name, rating=rating, comment=comment)
            feedbacks.save()
            return redirect('/')
        else:
            return redirect('/')

    else:
        form = FeedbackForm()
        return render(request, "feedback.html", {'form': form})


def academics(request):
    subject_dict = {1: 'Environmental Engineering', 2: 'Electro-Magnetic Field Theory', 3: 'Accounting',
                    4: 'Engineering Drawing', 5: 'Machine Learning', 6: 'Statistics', 7: 'Ethics',
                    8: 'Data Structure & Algorithms', 9: 'Network Theory'}
    user_id = request.user.id
    if request.method == "POST":
        sem = int(request.POST.get('sem'))
        subjects = request.POST.getlist('your_role')
        subject_marks_info = request.POST.getlist('fname')

        subject_marks = {subject_dict[int(subjects[0])]: int(subject_marks_info[0]),
                         subject_dict[int(subjects[1])]: int(subject_marks_info[1]),
                         subject_dict[int(subjects[2])]: int(subject_marks_info[2]),
                         subject_dict[int(subjects[3])]: int(subject_marks_info[3]),
                         }

        # calculate semester marks
        semester_marks = {sem: int(subject_marks_info[0]) + int(subject_marks_info[1]) + int(subject_marks_info[2]) + \
                               int(subject_marks_info[3])}

        least_interested_sub = []
        for i in subject_marks:
            if subject_marks[i] < 55:
                least_interested_sub.append(i)

        sub_sug_arr = suggested_subject.objects.filter(student_id=user_id).values().get()['suggested_subjects'][
            'suggested_subjects']

        common_least_int_sub = []
        least_interested_sub_set = set(least_interested_sub)
        sub_sug_arr_set = set(sub_sug_arr)

        if len(least_interested_sub_set.intersection(sub_sug_arr_set)) > 0:
            common_least_int_sub.append(least_interested_sub_set.intersection(sub_sug_arr_set))

        new_common_Sub = []

        for i in least_interested_sub_set:
            new_common_Sub.append(i)

        sub_tags = []

        student_data = student_score.objects.filter(student_id=user_id).values()[0]
        del student_data['id']
        del student_data['student_id']

        for ele in list(student_data):
            if student_data[ele] == False:
                student_data.pop(ele)

        student_data_arr = list(student_data)
        student_data_set = set(student_data_arr)

        for i in range(len(new_common_Sub)):
            sub_id = list(subject_dict.keys())[list(subject_dict.values()).index(new_common_Sub[i])]
            sub_data = subject.objects.filter(id=sub_id).values()[0]
            del sub_data['id']
            del sub_data['subject_name']
            all_keys = list(student_data.keys())
            subject_data_arr = []
            for ele in all_keys:
                if sub_data[ele]:
                    subject_data_arr.append(ele)
            subject_data_arr_set = set(subject_data_arr)
            if len(student_data_set.intersection(subject_data_arr_set)) > 0:
                student_data_set = student_data_set.intersection(subject_data_arr_set)

        for i in student_data_set:
            sub_tags.append(i)

        final_student_tag = student_score.objects.filter(student_id=user_id).values()[0]

        for i in sub_tags:
            for j in list(final_student_tag):
                if i == j:
                    final_student_tag[j] = False

        organised = final_student_tag['organised']
        stubborn = final_student_tag['stubborn']
        introvert = final_student_tag['introvert']
        extrovert = final_student_tag['extrovert']
        agreeable = final_student_tag['agreeable']
        passive = final_student_tag['passive']
        creative = final_student_tag['creative']
        unpredictable = final_student_tag['unpredictable']
        neurotic = final_student_tag['neurotic']
        regularity = final_student_tag['regularity']
        efficiency = final_student_tag['efficiency']
        teamwork = final_student_tag['teamwork']
        memory = final_student_tag['memory']
        psa = final_student_tag['psa']
        business = final_student_tag['business']
        management = final_student_tag['management']
        technical = final_student_tag['technical']
        entrepreneur = final_student_tag['entrepreneur']
        versatility = final_student_tag['versatility']
        space = final_student_tag['space']
        path_finding = final_student_tag['path_finding']
        data_handling = final_student_tag['data_handling']

        student_score.objects.filter(student_id=user_id).update(organised=organised, stubborn=stubborn,
                                                                introvert=introvert,
                                                                extrovert=extrovert, agreeable=agreeable,
                                                                passive=passive,
                                                                creative=creative, unpredictable=unpredictable,
                                                                neurotic=neurotic,
                                                                regularity=regularity, efficiency=efficiency,
                                                                teamwork=teamwork,
                                                                memory=memory, psa=psa, business=business,
                                                                management=management,
                                                                technical=technical, entrepreneur=entrepreneur,
                                                                versatility=versatility, space=space,
                                                                path_finding=path_finding,
                                                                data_handling=data_handling)

        if not Student_Report.objects.filter(student_id=user_id).exists():
            student = Student_Report.objects.create(student_id=user_id, subject_marks={sem: subject_marks},
                                                    semester_marks=semester_marks)
            student.save()
            return redirect('dashboard')

        else:
            # import pdb
            # pdb.set_trace()
            all_data = Student_Report.objects.filter(student_id=user_id).values().get()

            # whether same sem

            all_sem = list(all_data['subject_marks'].keys())
            for i in all_sem:
                if i == str(sem):
                    all_data['subject_marks'][i] = subject_marks
                    all_data['semester_marks'][i] = semester_marks[sem]

                    Student_Report.objects.update(subject_marks=all_data['subject_marks'],
                                                  semester_marks=all_data['semester_marks'])
                    # student.save()
                    return redirect('dashboard')
            else:

                new_subject_marks = all_data['subject_marks']
                new_subject_marks[str(sem)] = subject_marks
                new_sem_marks = all_data['semester_marks']
                new_sem_marks[str(sem)] = semester_marks[sem]
                Student_Report.objects.update(subject_marks=new_subject_marks, semester_marks=new_sem_marks)
                return redirect('dashboard')
    else:
        return render(request, 'academics.html')
