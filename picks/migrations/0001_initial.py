# Generated by Django 3.0.8 on 2020-10-12 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collecting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='s_images/', verbose_name='이미지')),
                ('content', models.TextField(verbose_name='내용')),
                ('collection_name', models.CharField(max_length=100, verbose_name='컬렉션명')),
                ('collection_products', models.TextField(verbose_name='컬렉션 상품')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
            ],
            options={
                'verbose_name': '공유',
                'verbose_name_plural': '공유',
            },
        ),
        migrations.CreateModel(
            name='CollectionProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qunatity', models.PositiveSmallIntegerField(verbose_name='수량')),
                ('sub_total', models.PositiveIntegerField(verbose_name='가격')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.Product', verbose_name='상품')),
            ],
            options={
                'verbose_name': '컬렉션상품',
                'verbose_name_plural': '컬렉션상품',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_total', models.PositiveIntegerField(default=0, verbose_name='가격')),
                ('period', models.CharField(blank=True, choices=[('1W', '1주'), ('2W', '2주'), ('3W', '3주'), ('1M', '1달'), ('2M', '2달'), ('3M', '3달')], max_length=2, verbose_name='배송주기')),
                ('name', models.CharField(max_length=100, verbose_name='컬렉션명')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('collection_products', models.ManyToManyField(blank=True, related_name='collection_products', through='picks.Collecting', to='picks.CollectionProduct', verbose_name='컬렉션 상품')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'verbose_name': '컬렉션',
                'verbose_name_plural': '컬렉션',
            },
        ),
        migrations.AddField(
            model_name='collecting',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picks.Collection', verbose_name='컬렉션'),
        ),
        migrations.AddField(
            model_name='collecting',
            name='collection_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picks.CollectionProduct', verbose_name='컬렉션 상품'),
        ),
        migrations.AlterUniqueTogether(
            name='collecting',
            unique_together={('collection', 'collection_product')},
        ),
    ]