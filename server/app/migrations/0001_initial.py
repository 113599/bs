# Generated by Django 4.1.3 on 2023-02-25 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Colleges',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录编号')),
                ('name', models.CharField(max_length=32, verbose_name='学院名称')),
                ('createTime', models.CharField(db_column='create_time', max_length=19, verbose_name='添加时间')),
            ],
            options={
                'db_table': 'fater_colleges',
            },
        ),
        migrations.CreateModel(
            name='Grades',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录编号')),
                ('name', models.CharField(max_length=32, verbose_name='班级名称')),
                ('createTime', models.CharField(db_column='create_time', max_length=19, verbose_name='添加时间')),
            ],
            options={
                'db_table': 'fater_grades',
            },
        ),
        migrations.CreateModel(
            name='Notices',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录编号')),
                ('title', models.CharField(max_length=32, verbose_name='公告标题')),
                ('detail', models.CharField(max_length=256, verbose_name='公告详情')),
                ('putTime', models.CharField(db_column='put_time', max_length=19, verbose_name='发布时间')),
            ],
            options={
                'db_table': 'fater_notices',
            },
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录编号')),
                ('name', models.CharField(max_length=32, verbose_name='科目名称')),
                ('createTime', models.CharField(db_column='create_time', max_length=19, verbose_name='添加时间')),
            ],
            options={
                'db_table': 'fater_projects',
            },
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11, verbose_name='联系电话')),
                ('record', models.CharField(max_length=10, verbose_name='教师学历 ')),
            ],
            options={
                'db_table': 'fater_teachers',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='用户编号')),
                ('userName', models.CharField(db_column='user_name', max_length=32, verbose_name='用户账号')),
                ('passWord', models.CharField(db_column='pass_word', max_length=32, verbose_name='用户密码')),
                ('name', models.CharField(max_length=20, verbose_name='用户姓名')),
                ('gender', models.CharField(max_length=4, verbose_name='用户性别')),
                ('age', models.IntegerField(verbose_name='用户年龄')),
                ('type', models.IntegerField(verbose_name='用户身份 0-管理员 1-教师 2-学生')),
            ],
            options={
                'db_table': 'fater_users',
            },
        ),
        migrations.CreateModel(
            name='Works',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录编号')),
                ('job', models.IntegerField(verbose_name='工作职责 0-授课教师 1-班主任')),
                ('grade', models.ForeignKey(db_column='grade_id', on_delete=django.db.models.deletion.CASCADE, to='app.grades')),
                ('project', models.ForeignKey(db_column='project_id', on_delete=django.db.models.deletion.CASCADE, to='app.projects')),
                ('teacher', models.ForeignKey(db_column='teacher_id', on_delete=django.db.models.deletion.CASCADE, to='app.teachers')),
            ],
            options={
                'db_table': 'fater_works',
            },
        ),
        migrations.AddField(
            model_name='teachers',
            name='user',
            field=models.OneToOneField(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='app.users'),
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(verbose_name='学生正常 0-正常 1-请假')),
                ('college', models.ForeignKey(db_column='college_id', on_delete=django.db.models.deletion.CASCADE, to='app.colleges')),
                ('grade', models.ForeignKey(db_column='grade_id', on_delete=django.db.models.deletion.CASCADE, to='app.grades')),
                ('user', models.OneToOneField(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='app.users')),
            ],
            options={
                'db_table': 'fater_students',
            },
        ),
        migrations.CreateModel(
            name='LeaveLogs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录编号')),
                ('reason', models.CharField(max_length=125, verbose_name='请假原由')),
                ('createTime', models.CharField(db_column='create_time', max_length=19, verbose_name='申请时间')),
                ('replyTime', models.CharField(db_column='reply_time', max_length=19, null=True, verbose_name='处理时间')),
                ('replyComm', models.CharField(db_column='reply_comm', max_length=125, null=True, verbose_name='回复原由')),
                ('status', models.IntegerField(verbose_name='处理状态 0-提交待审核 1-同意 2-驳回 3-销假')),
                ('student', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, to='app.students')),
                ('teacher', models.ForeignKey(db_column='teacher_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.teachers')),
            ],
            options={
                'db_table': 'fater_leave_logs',
            },
        ),
        migrations.CreateModel(
            name='Checks',
            fields=[
                ('no', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='考勤号码')),
                ('createTime', models.CharField(db_column='create_time', max_length=19, verbose_name='添加时间')),
                ('status', models.IntegerField(verbose_name='考勤状态 0-考勤中 1-考勤结束')),
                ('grade', models.ForeignKey(db_column='grade_id', on_delete=django.db.models.deletion.CASCADE, to='app.grades')),
                ('teacher', models.ForeignKey(db_column='teacher_id', on_delete=django.db.models.deletion.CASCADE, to='app.teachers')),
            ],
            options={
                'db_table': 'fater_checks',
            },
        ),
        migrations.CreateModel(
            name='CheckLogs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录编号')),
                ('createTime', models.CharField(db_column='create_time', max_length=19, verbose_name='考勤时间')),
                ('checks', models.ForeignKey(db_column='check_id', on_delete=django.db.models.deletion.CASCADE, to='app.checks')),
                ('student', models.ForeignKey(db_column='student_id', on_delete=django.db.models.deletion.CASCADE, to='app.students')),
            ],
            options={
                'db_table': 'fater_check_logs',
            },
        ),
    ]
