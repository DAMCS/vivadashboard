# Generated by Django 2.1 on 2018-08-27 23:38

from django.db import migrations, models
import django.db.models.deletion
import util.types


class Migration(migrations.Migration):

    dependencies = [
        ('VMS', '0005_student_address_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='report_submission_status',
            field=models.CharField(default='Pending', max_length=20),
        ),
        migrations.AddField(
            model_name='student',
            name='session',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='VMS.VMS_Session'),
        ),
        migrations.AddField(
            model_name='tutor',
            name='isIDFSent',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='tutor',
            name='isRSDFSent',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='logged_in_time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='batch',
            name='session',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='VMS.VMS_Session'),
        ),
        migrations.AlterField(
            model_name='guidestudentmap',
            name='session',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='VMS.VMS_Session'),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='session',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='VMS.VMS_Session'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_role',
            field=models.CharField(choices=[('Administrator', util.types.UserRoles('Administrator')), ('Viva Coordinator', util.types.UserRoles('Viva Coordinator')), ('Tutor', util.types.UserRoles('Tutor')), ('Guide', util.types.UserRoles('Guide')), ('Guest', util.types.UserRoles('Guest'))], max_length=50),
        ),
    ]