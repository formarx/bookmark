# Generated by Django 3.1.5 on 2021-01-21 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('appr_line', models.CharField(choices=[('A', '결재'), ('B', '합의'), ('C', '참조')], default='A', max_length=1)),
                ('appr_priorty', models.IntegerField(default=0)),
                ('appr_state', models.CharField(choices=[('YET', '미결'), ('YES', '결재'), ('NO', '반려')], default='YET', max_length=3)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='board.post')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
