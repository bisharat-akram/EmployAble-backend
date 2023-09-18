# Generated by Django 4.2.5 on 2023-09-18 09:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_managers_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.TextField()),
                ('description', models.TextField(max_length=1000)),
                ('phone_number', models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(code=400, message='Mobile is not in correct format', regex='^\\+?1?\\d{9,15}$')])),
                ('prior_highest_education', models.IntegerField(choices=[(1, 'Less than GED'), (2, 'GED'), (3, 'Some college'), (4, 'Associate`s'), (5, 'Bachelor`s'), (6, 'Master`s'), (7, 'Doctoral')])),
                ('interested_jobs', models.ManyToManyField(to='user.jobs')),
                ('skills', models.ManyToManyField(to='user.skills')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', related_query_name='user_profile', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer_name', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employment_history', related_query_name='employment_history', to='user.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree_type', models.IntegerField(choices=[(1, 'High School'), (2, "Bachelor's")])),
                ('major', models.CharField(max_length=50)),
                ('university_name', models.CharField(max_length=50)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education_history', related_query_name='education_history', to='user.userprofile')),
            ],
        ),
    ]