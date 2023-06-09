# Generated by Django 3.0.7 on 2023-05-09 20:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=10, verbose_name='닉네임')),
                ('profile_image', models.ImageField(default='images/default_profile.jpg', upload_to='profile_images/', verbose_name='프로필 이미지')),
                ('profile_address', models.CharField(max_length=300, verbose_name='프로필 주소')),
                ('phone', models.CharField(max_length=20, verbose_name='연락처')),
                ('address1', models.CharField(max_length=300, verbose_name='주소1')),
                ('address2', models.CharField(max_length=300, verbose_name='주소2 참고항목')),
                ('detail_address', models.CharField(max_length=300, verbose_name='상세주소')),
                ('zipcode', models.CharField(max_length=5, verbose_name='우편번호')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'verbose_name': '프로필',
                'verbose_name_plural': '프로필',
            },
        ),
    ]
