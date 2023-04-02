from django.shortcuts import render,redirect
from . utilities import load_data , student_perfomance_prediction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate ,logout
from .models import school_user
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from . forms import NewUserForm
from . models import school_user
# Create your views here.

@login_required
def homepage(request):
    student = load_data()


    students_passed = student['Pass/Fail'].value_counts().P
    students_failed = student['Pass/Fail'].value_counts().F
    male_count = student['gender'].value_counts().male
    female_count = student['gender'].value_counts().female

    total_students = student.count().iloc[0]

    # femal and male analytics
    female_passed = student[(student['gender']=='female') & (student['Pass/Fail']=='P')].shape[0]
    female_failed = student[(student['gender']=='female') & (student['Pass/Fail']=='F')].shape[0]
    female_data =  [female_passed,female_failed]

    male_passed = student[(student['gender']=='male') & (student['Pass/Fail']=='P')].shape[0]
    male_failed = student[(student['gender']=='male') & (student['Pass/Fail']=='F')].shape[0]
    male_data =  [male_passed,male_failed]

    male_math = int(student.loc[student['gender'] == 'male', 'math score'].mean())
    male_reading = int(student.loc[student['gender'] == 'male', 'reading score'].mean())
    male_writing = int(student.loc[student['gender'] == 'male', 'writing score'].mean())
    male_scores = [male_math,male_reading,male_writing]

    female_math = int(student.loc[student['gender'] == 'female', 'math score'].mean())
    female_reading = int(student.loc[student['gender'] == 'female', 'reading score'].mean())
    female_writing = int(student.loc[student['gender'] == 'female', 'writing score'].mean())
    female_scores = [female_math,female_reading,female_writing]

    education_level_perc = []
    unique_education = [x for x in student['parental level of education'].unique()]

    for i in student['parental level of education'].unique():

        education_passed = student[(student['Pass/Fail']=='P')&(student['parental level of education']==i)].count().iloc[0]
        total = student[(student['parental level of education']==i)].count().iloc[0]

        education_level_perc.append(int((education_passed/total)*100))
    print(education_level_perc)



    standars_lunch_passed = student[(student['lunch']=='standard') & (student['Pass/Fail']=='P')].shape[0]
    standars_lunch_failed = student[(student['lunch']=='standard') & (student['Pass/Fail']=='F')].shape[0]
    standard_lunch =  [standars_lunch_passed,standars_lunch_failed]

    reduced_lunch_passed = student[(student['lunch']=='standard') & (student['Pass/Fail']=='P')].shape[0]
    reduced_lunch_passed = student[(student['lunch']=='free/reduced') & (student['Pass/Fail']=='F')].shape[0]
    reduced_lunch =  [reduced_lunch_passed,reduced_lunch_passed]
    context = {'students_info':[total_students,students_passed,students_failed,male_count,female_count],'male_data':male_data,'female_data':female_data,'male_scores':male_scores,'female_scores':female_scores,'education_level_perc':education_level_perc,'unique_education':unique_education,'standard_lunch':standard_lunch,'reduced_lunch':reduced_lunch}


    return render(request, 'index.html',context)

@login_required
def analytics(request):
    #loading dataset
    student = load_data()


    students_passed = student['Pass/Fail'].value_counts().P
    students_failed = student['Pass/Fail'].value_counts().F
    male_count = student['gender'].value_counts().male
    female_count = student['gender'].value_counts().female

    total_students = student.count().iloc[0]

    # femal and male analytics
    female_passed = student[(student['gender']=='female') & (student['Pass/Fail']=='P')].shape[0]
    female_failed = student[(student['gender']=='female') & (student['Pass/Fail']=='F')].shape[0]
    female_data =  [female_passed,female_failed]

    male_passed = student[(student['gender']=='male') & (student['Pass/Fail']=='P')].shape[0]
    male_failed = student[(student['gender']=='male') & (student['Pass/Fail']=='F')].shape[0]
    male_data =  [male_passed,male_failed]

    male_math = int(student.loc[student['gender'] == 'male', 'math score'].mean())
    male_reading = int(student.loc[student['gender'] == 'male', 'reading score'].mean())
    male_writing = int(student.loc[student['gender'] == 'male', 'writing score'].mean())
    male_scores = [male_math,male_reading,male_writing]

    female_math = int(student.loc[student['gender'] == 'female', 'math score'].mean())
    female_reading = int(student.loc[student['gender'] == 'female', 'reading score'].mean())
    female_writing = int(student.loc[student['gender'] == 'female', 'writing score'].mean())
    female_scores = [female_math,female_reading,female_writing]

    education_level_perc = []
    unique_education = [x for x in student['parental level of education'].unique()]

    for i in student['parental level of education'].unique():

        education_passed = student[(student['Pass/Fail']=='P')&(student['parental level of education']==i)].count().iloc[0]
        total = student[(student['parental level of education']==i)].count().iloc[0]

        education_level_perc.append(int((education_passed/total)*100))
    print(education_level_perc)



    standars_lunch_passed = student[(student['lunch']=='standard') & (student['Pass/Fail']=='P')].shape[0]
    standars_lunch_failed = student[(student['lunch']=='standard') & (student['Pass/Fail']=='F')].shape[0]
    standard_lunch =  [standars_lunch_passed,standars_lunch_failed]

    reduced_lunch_passed = student[(student['lunch']=='standard') & (student['Pass/Fail']=='P')].shape[0]
    reduced_lunch_passed = student[(student['lunch']=='free/reduced') & (student['Pass/Fail']=='F')].shape[0]
    reduced_lunch =  [reduced_lunch_passed,reduced_lunch_passed]
    context = {'students_info':[total_students,students_passed,students_failed,male_count,female_count],'male_data':male_data,'female_data':female_data,'male_scores':male_scores,'female_scores':female_scores,'education_level_perc':education_level_perc,'unique_education':unique_education,'standard_lunch':standard_lunch,'reduced_lunch':reduced_lunch}


    return render(request, 'analytics.html',context)

@login_required
def students_list(request):
    student = load_data()
    student.insert(0,'id',student.index)
    student.drop(['Unnamed: 0.1', 'Unnamed: 0'], axis=1,inplace = True)
    context = {'df':student}
    return render(request, 'students_list.html',context)

@login_required
def registered_users(request):
    registered_users= school_user.objects.all()
    context = {'registered_users':registered_users}
    return render(request, 'registered_users.html',context)

@login_required
def prediction(request):
    if request.method == "POST":
        gender= request.POST["gender"]
        race= request.POST["race"]
        parent_edu= request.POST["parent_edu"]
        lunch= request.POST["lunch"]
        prep_course= request.POST["prep_course"]

        result = student_perfomance_prediction(gender, race, parent_edu, lunch , prep_course)
        result = int(result[0]*100)
        print("result:" ,result)

        return render(request, 'prediction_form.html',{'result': result})

    return render(request, 'prediction_form.html')

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():

            user = form.save()
            scho_user = school_user(user=user,email=user.email)
            scho_user.save()
            login(request, user)
            return redirect("/")
    form = NewUserForm()
    return render (request=request, template_name="registration/register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect("homepage")

    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form":form})

def logout_view(request):
    logout(request)
    return redirect('login')

def aboutus(request):
    return render(request, 'aboutus.html')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            print(associated_users)
            if associated_users.exists():
                print("g")
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("accounts/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})
