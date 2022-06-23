import email
from pyexpat.errors import messages

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import *
from django.shortcuts import render, redirect
from datetime import date


def index(request):

    jobs = Job.objects.all().order_by('end_date')
    feedback = Feedback.objects.all()
    return render(request, "index.html", {'jobs': jobs,'feedback': feedback }, )


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            user1 = Personal_info.objects.get(user=user)
            if user1.type == "applicant":
                login(request, user)
                return redirect("/user_homepage", )
        else:
            thank = True
            return render(request, "user_login.html", {"thank": thank})
    return render(request, "user_login.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                        password=password1, email=email)
        applicants = Personal_info.objects.create(user=user, email=email, phone=phone, type="applicant")
        user.save()
        applicants.save()
        return render(request, "user_login.html")
    return render(request, "create_user.html")


def logout(request):
    return redirect('/')


def user_homepage(request):
    applicant = Personal_info.objects.get(user=request.user)
    jobs = Job.objects.all().order_by('end_date')
    my_list = Application.objects.filter(applicant=applicant)
    return render(request, "user_homepage.html", {'jobs': jobs, 'my_list': my_list})


def company_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        cemail = request.POST['email']
        regid = request.POST.get('regid')
        curl = request.POST.get('curl')
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        company_name = request.POST['company_name']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')

        user = User.objects.create_user(email=email, username=username, password=password1)
        company = Company.objects.create(user=user, phone=phone, company_name=company_name, curl=curl, regid=regid,
                                         email=cemail, type="company", status="pending")

        user.save()
        company.save()
        return render(request, "company_login.html")
    return render(request, "create_company.html")


def company_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            user1 = Company.objects.get(user=user)
            if user1.type == "company" and user1.status != "pending":
                login(request, user)
                return redirect("/company_homepage")
        else:
            alert = True
            return render(request, "company_login.html", {"alert": alert})

    return render(request, "company_login.html")


def company_homepage(request):
    applicant = Company.objects.get(user=request.user)
    my_list = Application.objects.filter(company=applicant)
    return render(request, "company_homepage.html", {'my_list': my_list})


def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user.is_superuser:
            login(request, user)
            return redirect("/admin_homepage")
        else:
            alert = True
            return render(request, "admin_login.html", {"alert": alert})
    return render(request, "admin_login.html")


def all_companies(request):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    companies = Company.objects.all()
    return render(request, "all_companies.html", {'companies': companies})


def admin_homepage(request):
    feedback=Feedback.objects.all()

    return render(request, "admin_homepage.html",{'feedback':feedback} )


def change_status(request, myid):
    if not request.user.is_authenticated:
        return redirect("/all_companies")
    company = Company.objects.get(id=myid)
    if request.method == "POST":
        status = request.POST['status']
        company.status = status
        company.save()
        alert = True
        return render(request, "change_status.html", {'alert': alert})
    return render(request, "change_status.html", {'company': company})


@login_required
def add_job(request):
    skl = Skills.objects.all()
    if not request.user.is_authenticated:
        return redirect("/company_login")
    if request.method == "POST":
        title = request.POST['job_title']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        salary = request.POST['salary']
        experience = request.POST['experience']
        location = request.POST['location']
        skills = request.POST['skills']
        extra_skills = request.POST['extra_skills']
        job_type = request.POST['job_type']
        description = request.POST['description']
        vacancies = request.POST['vacancies']
        user = request.user
        company = Company.objects.get(user=user)
        job = Job.objects.create(company=company, title=title, start_date=start_date, extra_skills=extra_skills,
                                 job_type=job_type, vacancies=vacancies, end_date=end_date, salary=salary,
                                 experience=experience, location=location, skills=skills, description=description,
                                 creation_date=date.today())
        job.save()
        alert = True
        return render(request, "add_job.html", {'alert': alert})
    return render(request, "add_job.html", context={'skills': skl})


def job_list(request):
    if not request.user.is_authenticated:
        return redirect("/company_login")
    companies = Company.objects.get(user=request.user)
    jobs = Job.objects.order_by('-creation_date').filter(company=companies)
    return render(request, "job_list.html", {'jobs': jobs})


def edit_job(request, myid):
    if not request.user.is_authenticated:
        return redirect("/job_list")
    skl = Skills.objects.all()
    job = Job.objects.get(id=myid)
    if request.method == "POST":
        title = request.POST['job_title']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        salary = request.POST['salary']
        experience = request.POST['experience']
        location = request.POST['location']
        skills = request.POST['skills']
        description = request.POST['description']

        job.title = title
        job.salary = salary
        job.experience = experience
        job.location = location
        job.skills = skills
        job.description = description

        job.save()
        if start_date:
            job.start_date = start_date
            job.save()
        if end_date:
            job.end_date = end_date
            job.save()
        alert = True
        return render(request, "edit_job.html", {'alert': alert})
    return render(request, "edit_job.html", context={'job': job, 'skills': skl}, )


def feedbacks(request):
    feedbacks = Feedback.objects.all()

    return render(request, "user_feedback.html", {'feedbacks': feedbacks})


def all_jobs(request):
    jobs = Job.objects.all().order_by('-start_date')
    applicant = Personal_info.objects.get(user=request.user)
    apply = Application.objects.filter(applicant=applicant)
    data = []
    for i in apply:
        data.append(i.job.id)
    return render(request, "all_jobs.html", {'jobs': jobs, 'data': data})


def job_apply(request, myid):
    if not request.user.is_authenticated:
        return redirect("/user_login")
    applicant = Personal_info.objects.get(user=request.user)
    job = Job.objects.get(id=myid)
    date1 = date.today()
    if job.end_date < date1:
        closed = True
        return render(request, "job_apply.html", {'closed': closed})
    elif job.start_date > date1:
        notopen = True
        return render(request, "job_apply.html", {'notopen': notopen})
    else:
        if request.method == "POST":
            resume = request.FILES['resume']
            Application.objects.create(job=job, company=job.company, applicant=applicant, resume=resume,
                                       apply_date=date.today(),status='Pending')
            alert = True
            return render(request, "all.html", {'alert': alert})
    return render(request, "job_apply.html", {'job': job})


def all(request):
    jobs = Job.objects.all().order_by('end_date')
    search = Job.objects.all()
    applicant = Personal_info.objects.get(user=request.user)
    apply = Application.objects.filter(applicant=applicant)
    data = []
    for i in apply:
        data.append(i.job.id)
    if request.method == "POST":
        title = request.POST['title']
        company = request.POST['company']
        location = request.POST['location']
        search = Job.objects.all()
        jobs = Job.objects.filter(title=title, company_id=company, location=location)
        return render(request, "all.html", {'jobs': jobs, 'search': search})
    return render(request, "all.html", {'jobs': jobs, 'data': data,'search':search},)


def job_details(request, myid):
    jobs = Job.objects.get(id=myid)
    return render(request, "job_details.html", {'jobs': jobs})


def user_profile(request):
    applicant = Personal_info.objects.get(user=request.user)
    if request.method == "POST":

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        gender = request.POST['gender']
        email = request.POST['email']

        applicant.user.email = email
        applicant.user.first_name = first_name
        applicant.user.last_name = last_name
        applicant.phone = phone
        applicant.gender = gender
        applicant.save()
        applicant.user.save()

        try:
            image = request.FILES['image']
            applicant.image = image
            applicant.save()
        except:
            pass
        alert = True
        return render(request, "user_homepage.html", {'alert': alert})
    return render(request, 'user_profile.html', {'applicant': applicant}, )


def all_applicants(request):
    company = Company.objects.get(user=request.user)
    application = Application.objects.filter(company=company)
    return render(request, "all_applicants.html", {'application': application})


def job_search(request):
    search = Job.objects.all()
    jobs = Job.objects.all()

    if request.method == "POST":
        title = request.POST['title']
        company = request.POST['company']
        location = request.POST['location']
        search = Job.objects.all()
        jobs = Job.objects.filter(title=title, company_id=company, location=location)
        return render(request, "all.html", {'jobs': jobs, 'search': search})
    return render(request, "job_search.html", {'jobs': jobs, 'search': search})


def job_full_time(request):
    jobs = Job.objects.filter(job_type='Full Time').order_by('end_date')
    applicant = Personal_info.objects.get(user=request.user)
    apply = Application.objects.filter(applicant=applicant)
    data = []
    for i in apply:
        data.append(i.job.id)
    return render(request, "job_full_time.html", {'jobs': jobs, 'data': data})


def job_part_time(request):
    jobs = Job.objects.filter(job_type='Part Time').order_by('end_date')
    applicant = Personal_info.objects.get(user=request.user)
    apply = Application.objects.filter(applicant=applicant)
    data = []
    for i in apply:
        data.append(i.job.id)
    return render(request, "job_part_time.html", {'jobs': jobs, 'data': data})


def application_status(request, myid):
    applicant = Company.objects.get(user=request.user)
    my_list = Application.objects.filter(company=applicant)
    application = Application.objects.get(id=myid)
    if request.method == "POST":
        status = request.POST['status']
        application.status = status
        application.save()

        return render(request, "company_homepage.html",{'my_list': my_list},)
    return render(request, "company_homepage.html",{'my_list': my_list}, )


def feedback(request):
    if request.method == "POST":
        messages = request.POST['message']
        user=Personal_info.objects.get(user=request.user)
        Feedback.objects.create(message=messages, user=user,)
    return render(request, "feedback.html", )

def view_applicants(request):
    my_list=Personal_info.objects.all()
    return render(request, "view_applicants.html",{"my_list": my_list}, )

def delete_company(request, myid):
    if not request.user.is_authenticated:
        return redirect("/admin_login")
    company = User.objects.filter(id=myid)
    company.delete()
    return redirect("/all_companies")