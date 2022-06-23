# Generated by Django 3.2 on 2022-05-30 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('IPSR', '0005_rename_applicant_personal_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10)),
                ('type', models.CharField(max_length=15)),
                ('status', models.CharField(max_length=20)),
                ('company_name', models.CharField(max_length=100)),
                ('regid', models.CharField(max_length=20)),
                ('curl', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
