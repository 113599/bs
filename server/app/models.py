from django.db import models

# 公告信息
class Notices(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    title = models.CharField('公告标题',  max_length=32, null=False)
    detail = models.CharField('公告详情', max_length=256, null=False)
    putTime = models.CharField('发布时间', db_column='put_time', max_length=19)
    class Meta:
        db_table = 'fater_notices'

# 学院信息
class Colleges(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('学院名称',  max_length=32, null=False)
    createTime = models.CharField('添加时间', db_column='create_time', max_length=19)
    class Meta:
        db_table = 'fater_colleges'

# 班级信息
class Grades(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('班级名称',  max_length=32, null=False)
    createTime = models.CharField('添加时间', db_column='create_time', max_length=19)
    class Meta:
        db_table = 'fater_grades'

# 课程信息
class Projects(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    name = models.CharField('科目名称',  max_length=32, null=False)
    createTime = models.CharField('添加时间', db_column='create_time', max_length=19)
    class Meta:
        db_table = 'fater_projects'

# 用户信息
class Users(models.Model):
    id = models.CharField('用户编号', max_length=20, null=False, primary_key=True)
    userName = models.CharField('用户账号', db_column='user_name', max_length=32, null=False)
    passWord = models.CharField('用户密码', db_column='pass_word', max_length=32, null=False)
    name = models.CharField('用户姓名', max_length=20, null=False)
    gender = models.CharField('用户性别', max_length=4, null=False)
    age = models.IntegerField('用户年龄', null=False)
    type = models.IntegerField('用户身份 0-管理员 1-教师 2-学生', null=False)
    class Meta:
        db_table = 'fater_users'

# 学生信息
class Students(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, db_column="user_id")
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE, db_column="grade_id")
    college = models.ForeignKey(Colleges, on_delete=models.CASCADE, db_column="college_id")
    status = models.IntegerField('学生正常 0-正常 1-请假', null=False)
    class Meta:
        db_table = 'fater_students'

# 教师信息
class Teachers(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, db_column="user_id")
    phone = models.CharField('联系电话', max_length=11, null=False)
    record = models.CharField('教师学历 ', max_length=10, null=False)
    class Meta:
        db_table = 'fater_teachers'

# 工作安排
class Works(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, db_column="teacher_id")
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, db_column="project_id")
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE, db_column="grade_id")
    job = models.IntegerField('工作职责 0-授课教师 1-班主任', null=False)
    class Meta:
        db_table = 'fater_works'

# 考勤处理
class Checks(models.Model):
    no = models.CharField('考勤号码', max_length=20, null=False, primary_key=True)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, db_column="teacher_id")
    grade = models.ForeignKey(Grades, on_delete=models.CASCADE, db_column="grade_id")
    createTime = models.CharField('添加时间', db_column='create_time', max_length=19)
    status = models.IntegerField('考勤状态 0-考勤中 1-考勤结束', null=False)
    class Meta:
        db_table = 'fater_checks'

# 考勤记录
class CheckLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    checks = models.ForeignKey(Checks, on_delete=models.CASCADE, db_column="check_id")
    student = models.ForeignKey(Students, on_delete=models.CASCADE, db_column="student_id")
    createTime = models.CharField('考勤时间', db_column='create_time', max_length=19)
    class Meta:
        db_table = 'fater_check_logs'

# 请假记录
class LeaveLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    reason = models.CharField('请假原由', max_length=125, null=False)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, db_column="student_id")
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, db_column="teacher_id", null=True)
    createTime = models.CharField('申请时间', db_column='create_time', max_length=19)
    replyTime = models.CharField('处理时间', db_column='reply_time', max_length=19, null=True)
    replyComm = models.CharField('回复原由', db_column='reply_comm', max_length=125, null=True)
    status = models.IntegerField('处理状态 0-提交待审核 1-同意 2-驳回 3-销假', null=False)
    class Meta:
        db_table = 'fater_leave_logs'