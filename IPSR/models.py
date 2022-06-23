from django.contrib.auth.models import User
from django.db import models


class Personal_info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    image = models.ImageField(upload_to="")
    type = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.user.first_name


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    status = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
    regid = models.CharField(max_length=20)
    curl = models.CharField(max_length=300)
    email = models.EmailField()

    def __str__ (self):
        return self.user.username


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=200)
    salary = models.FloatField()
    description = models.TextField(max_length=400)
    experience = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    extra_skills = models.CharField(max_length=200)
    creation_date = models.DateField()
    vacancies = models.IntegerField()
    job_type = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Skills(models.Model):
    skill_name = models.CharField(max_length=30)

class Feedback(models.Model):
    user = models.ForeignKey(Personal_info, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)



class Application(models.Model):
    company = models.CharField(max_length=200, default="")
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Personal_info, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    resume = models.ImageField(upload_to="")
    apply_date = models.DateField()

    def __str__ (self):
        return str(self.applicant)