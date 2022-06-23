from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("job_search/", views.job_search, name="job_search"),
    path("user_login/", views.user_login, name="user_login"),
    path("Create User/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("user_homepage/", views.user_homepage, name="user_homepage"),
    path("all_jobs/", views.all_jobs, name="all_jobs"),
    path("all/", views.all, name="all"),
    path("job_full_time/", views.job_full_time, name="job_full_time"),
    path("job_part_time/", views.job_part_time, name="job_part_time"),
    path("job_details/<int:myid>/",views.job_details, name="job_details"),
    path("job_apply/<int:myid>/",views.job_apply, name="job_apply"),

    path("user_profile/",views.user_profile, name="user_profile"),
    path("feedback/",views.feedback, name="feedback"),


    #company
    path("company_signup/", views.company_signup, name="company_signup"),
    path("company_login/", views.company_login, name="company_login"),
    path("company_homepage/", views.company_homepage, name="company_homepage"),
    path("add_job/", views.add_job, name="add_job"),
    path("job_list/", views.job_list, name="job_list"),
    path("all_applicants/", views.all_applicants, name="all_applicants"),
    path("edit_job/<int:myid>/", views.edit_job, name="edit_job"),
    path("application_status/<int:myid>/", views.application_status, name="application_status"),


    # admin
    path("admin_login/", views.admin_login, name="admin_login"),
    path("all_companies/", views.all_companies, name="all_companies"),
    path("admin_homepage/", views.admin_homepage, name="admin_homepage"),
    path("change_status/<int:myid>/", views.change_status, name="change_status"),
    path("feedbacks/", views.feedbacks, name="feedbacks"),
    path("view_applicants/", views.view_applicants, name="view_applicants"),
    path("delete_company/<int:myid>/", views.delete_company, name="delete_company"),

]