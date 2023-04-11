import uuid

from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render

from app import models
from comm.BaseView import BaseView
from comm.CommUtils import DateUtil, SysUtil, CheckUtil

'''
系统处理
'''
class SysView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':
            return SysView.getUserInfo(request)
        else:
            return BaseView.error('请求地址不存在')

    def post(self, request, module, *args, **kwargs):

        if module == 'login':
            return SysView.login(request)
        elif module == 'exit':
            return SysView.exit(request)
        elif module == 'info':
            return SysView.updUserInfo(request)
        elif module == 'pwd':
            return SysView.updUserPwd(request)
        else:
            return BaseView.error('请求地址不存在')

    # 获取登陆用户
    def getUserInfo(request):

        user = models.Users.objects.filter(id=cache.get(request.GET.get('token'))).first()

        if user.type==0:

            return BaseView.successData({
                'id': user.id,
                'userName': user.userName,
                'name': user.name,
                'gender': user.gender,
                'age': user.age,
                'type': user.type,
            })
        elif user.type==1:

            teacher = models.Teachers.objects.filter(user__id=user.id).first()
            return BaseView.successData({
                'id': user.id,
                'userName': user.userName,
                'name': user.name,
                'gender': user.gender,
                'age': user.age,
                'type': user.type,
                'phone': teacher.phone,
                'record': teacher.record
            })
        else:
            student = models.Students.objects.filter(user__id=user.id).first()
            return BaseView.successData({
                'id': user.id,
                'userName': user.userName,
                'name': user.name,
                'gender': user.gender,
                'age': user.age,
                'type': user.type,
                'gradeId': student.grade.id,
                'gradeName': student.grade.name,
                'collegeId': student.college.id,
                'collegeName': student.college.name,
            })

    # 登陆处理
    def login(request):

        userName = request.POST.get('userName')
        passWord = request.POST.get('passWord')

        user = models.Users.objects.filter(userName=userName)
        if user.exists():
            user = user.first()
            if user.passWord == passWord:

                if request.POST.get('type')=='app':

                    if user.type == 2:
                        token = uuid.uuid4()
                        resl = {
                            'token': str(token)
                        }
                        cache.set(token, user.id, 60 * 60 * 60 * 3)
                        return SysView.successData(resl)
                    else:

                        return BaseView.warn('暂无此类操作权限')
                else:

                    if user.type == 2:

                        return BaseView.warn('暂无此类操作权限')
                    else:

                        token = uuid.uuid4()
                        resl = {
                            'token': str(token)
                        }
                        cache.set(token, user.id, 60 * 60 * 60 * 3)
                        return SysView.successData(resl)
            else:
                return SysView.warn('用户密码输入错误')
        else:
            return SysView.warn('用户名输入错误')

    # 退出系统
    def exit(request):

        cache.delete(request.POST.get('token'))
        return BaseView.success()

    # 修改登陆用户信息
    def updUserInfo(request):

        user = models.Users.objects.filter(id=cache.get(request.POST.get('token')))
        if (request.POST.get('userName') != user.first().userName) & \
                (models.Users.objects.filter(userName=request.POST.get('userName')).exists()):
            return BaseView.warn('用户账号已存在')
        else:
            user.update(
                userName=request.POST.get('userName'),
                name=request.POST.get('name'),
                gender=request.POST.get('gender'),
                age=request.POST.get('age'),
            )
            return BaseView.success()

    # 修改登陆用户密码
    def updUserPwd(request):

        user = models.Users.objects.filter(id=cache.get(request.POST.get('token')))


        if (request.POST.get('oldPwd') != user.first().passWord):

            return BaseView.warn('原始密码输入错误')
        elif (request.POST.get('newPwd') != request.POST.get('rePwd')):

            return BaseView.warn('两次输入的密码不一致')
        else:
            user.update(
                passWord=request.POST.get('newPwd')
            )
            return BaseView.success()


'''
系统公告处理
'''
class NoticesView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == "page":
            return NoticesView.getPageInfos(request)
        elif module == 'show':
            return NoticesView.getShow(request)
        else:
            return BaseView.error('请求地址不存在')

    def post(self, request, module, *args, **kwargs):

        if module == "add":
            return NoticesView.addInfo(request)
        elif module == 'del':
            return NoticesView.delInfo(request)
        else:
            return BaseView.error('请求地址不存在')

    # 分页查询公告信息
    def getPageInfos(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        title = request.GET.get('title')

        qruery = Q();

        if SysUtil.isExit(title):
            qruery = qruery & Q(title__contains=title)

        data = models.Notices.objects.filter(qruery).order_by('-putTime')

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            resl.append({
                'id': item.id,
                'title': item.title,
                'detail': item.detail,
                'putTime': item.putTime
            })

        pageData = BaseView.parasePage(int(pageIndex), int(pageSize),
                                       paginator.page(pageIndex).paginator.num_pages,
                                       paginator.count, resl)

        return BaseView.successData(pageData)

    # 获取要显示的最新公告信息
    def getShow(request):

        notices = models.Notices.objects.order_by('-putTime')

        if notices.exists():

            notice = notices.first()
            return BaseView.successData({
                "id": notice.id,
                "title": notice.title,
                "detail": notice.detail,
                "putTime": notice.putTime,
            })
        else:
            return BaseView.warn("未发布公告内容")

    # 添加公告信息
    def addInfo(request):

        models.Notices.objects.create(
            title=request.POST.get('title'),
            detail=request.POST.get('detail'),
            putTime=DateUtil.getNowDateTime()
        )
        return BaseView.success()

    # 删除公告信息
    def delInfo(request):

        models.Notices.objects.filter(id=request.POST.get('id')).delete()
        return BaseView.success()

'''
学院处理
'''
class CollegesView(BaseView):

    def get(self, request, module, *args, **kwargs):
        if module == 'all':
            return CollegesView.getAll(request)
        elif module == 'page':
            return CollegesView.getPageInfos(request)
        else:
            return BaseView.error('请求地址不存在')

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return CollegesView.addInfo(request)
        elif module == 'upd':
            return CollegesView.updInfo(request)
        elif module == 'del':
            return CollegesView.delInfo(request)
        else:
            return BaseView.error('请求地址不存在')

    # 获取全部的学院信息
    def getAll(request):

        colleges = models.Colleges.objects.all();

        return BaseView.successData(list(colleges.values()))

    # 分页获取学院信息
    def getPageInfos(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')

        qruery = Q();

        if SysUtil.isExit(name):
            qruery = qruery & Q(name__contains=name)

        data = models.Colleges.objects.filter(qruery).order_by('-createTime')

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            resl.append({
                'id': item.id,
                'name': item.name,
                'createTime': item.createTime
            })


        pageData = BaseView.parasePage(int(pageIndex), int(pageSize),
                                       paginator.page(pageIndex).paginator.num_pages,
                                       paginator.count, resl)

        return BaseView.successData(pageData)

    # 添加学院信息
    def addInfo(request):

        models.Colleges.objects.create(
            name=request.POST.get('name'),
            createTime=DateUtil.getNowDateTime()
        )
        return BaseView.success()

    # 修改学院信息
    def updInfo(request):

        models.Colleges.objects. \
            filter(id=request.POST.get('id')).update(
            name=request.POST.get('name')
        )
        return BaseView.success()

    # 删除学院信息
    def delInfo(request):

        if models.Students.objects.filter(college__id=request.POST.get('id')).exists():
            return BaseView.warn('存在关联记录无法移除')
        else:
            models.Colleges.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()

'''
课程信息处理
'''
class ProjectsView(BaseView):

    def get(self, request, module, *args, **kwargs):
        if module == 'all':
            return ProjectsView.getAll(request)
        elif module == 'page':
            return ProjectsView.getPageInfos(request)
        else:
            return BaseView.error('请求地址不存在')

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return ProjectsView.addInfo(request)
        elif module == 'upd':
            return ProjectsView.updInfo(request)
        elif module == 'del':
            return ProjectsView.delInfo(request)
        else:
            return BaseView.error('请求地址不存在')

    # 获取全部的科目信息
    def getAll(request):

        projects = models.Projects.objects.all();

        return BaseView.successData(list(projects.values()))

    # 分页获取科目信息
    def getPageInfos(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')

        qruery = Q();

        if SysUtil.isExit(name):
            qruery = qruery & Q(name__contains=name)

        data = models.Projects.objects.filter(qruery).order_by('-createTime')

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            resl.append({
                'id': item.id,
                'name': item.name,
                'createTime': item.createTime
            })


        pageData = BaseView.parasePage(int(pageIndex), int(pageSize),
                                       paginator.page(pageIndex).paginator.num_pages,
                                       paginator.count, resl)

        return BaseView.successData(pageData)

    # 添加科目信息
    def addInfo(request):

        models.Projects.objects.create(
            name=request.POST.get('name'),
            createTime=DateUtil.getNowDateTime()
        )
        return BaseView.success()

    # 修改科目信息
    def updInfo(request):

        models.Projects.objects. \
            filter(id=request.POST.get('id')).update(
            name=request.POST.get('name')
        )
        return BaseView.success()

    # 删除科目信息
    def delInfo(request):

        if (models.Works.objects.filter(project__id=request.POST.get('id')).exists()):

            return BaseView.warn('存在关联记录无法移除')
        else:

            models.Projects.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()

'''
班级信息管理
'''
class GradesView(BaseView):

    def get(self, request, module, *args, **kwargs):
        if module == 'all':
            return GradesView.getAll(request)
        elif module == 'page':
            return GradesView.getPageInfos(request)
        else:
            return BaseView.error('请求地址不存在')

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return GradesView.addInfo(request)
        elif module == 'upd':
            return GradesView.updInfo(request)
        elif module == 'del':
            return GradesView.delInfo(request)
        else:
            return BaseView.error('请求地址不存在')

    # 获取全部的班级信息
    def getAll(request):

        grades = models.Grades.objects.all();

        return BaseView.successData(list(grades.values()))

    # 分页获取班级信息
    def getPageInfos(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')

        qruery = Q();

        if SysUtil.isExit(name):
            qruery = qruery & Q(name__contains=name)

        data = models.Grades.objects.filter(qruery).order_by('-createTime')

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            resl.append({
                'id': item.id,
                'name': item.name,
                'createTime': item.createTime
            })

        pageData = BaseView.parasePage(int(pageIndex), int(pageSize),
                                       paginator.page(pageIndex).paginator.num_pages,
                                       paginator.count, resl)

        return BaseView.successData(pageData)

    # 添加班级信息
    def addInfo(request):

        models.Grades.objects.create(
            name=request.POST.get('name'),
            createTime=DateUtil.getNowDateTime()
        )
        return BaseView.success()

    # 修改班级信息
    def updInfo(request):

        models.Grades.objects. \
            filter(id=request.POST.get('id')).update(
            name=request.POST.get('name')
        )
        return BaseView.success()

    # 删除班级信息
    def delInfo(request):

        if models.Students.objects.filter(grade__id=request.POST.get('id')).exists():
            return BaseView.warn('存在关联学生无法移除')
        elif (models.Works.objects.filter(grade__id=request.POST.get('id')).exists() |
                models.Checks.objects.filter(grade__id=request.POST.get('id')).exists()):
            return BaseView.warn('存在关联记录无法移除')
        else:
            models.Grades.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()

'''
学生信息处理
'''
class StudentsView(BaseView):

    def get(self, request, module, *args, **kwargs):
        if module == 'page':
            return StudentsView.getPageInfos(request)
        elif module == 'info':
            return StudentsView.getInfo(request)
        else:
            return BaseView.error('请求地址不存在')

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return StudentsView.addInfo(request)
        elif module == 'upd':
            return StudentsView.updInfo(request)
        elif module == 'del':
            return StudentsView.delInfo(request)
        else:
            return BaseView.error('请求地址不存在')

    # 获取指定学生信息
    def getInfo(request):

        student = models.Students.objects.filter(user__id=request.GET.get('id')).first()

        return BaseView.successData({
            'id': student.user.id,
            'userName': student.user.userName,
            'passWord': student.user.passWord,
            'name': student.user.name,
            'gender': student.user.gender,
            'age': student.user.age,
            'gradeId': student.grade.id,
            'gradeName': student.grade.name,
            'collegeId': student.college.id,
            'collegeName': student.college.name,
            'status': student.status
        })

    #分页查询学生信息
    def getPageInfos(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        stuName = request.GET.get('stuName')
        collegeId = request.GET.get('collegeId')
        gradeId = request.GET.get('gradeId')

        qruery = Q();

        if SysUtil.isExit(stuName):
            qruery = qruery & Q(user__name__contains=stuName)

        if SysUtil.isExit(collegeId):
            qruery = qruery & Q(college__id=int(collegeId))

        if SysUtil.isExit(gradeId):
            qruery = qruery & Q(grade__id=int(gradeId))

        data = models.Students.objects.filter(qruery)

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            resl.append({
                'id': item.user.id,
                'userName': item.user.userName,
                'name': item.user.name,
                'gender': item.user.gender,
                'age': item.user.age,
                'gradeId': item.grade.id,
                'gradeName': item.grade.name,
                'collegeId': item.college.id,
                'collegeName': item.college.name,
                'status': item.status
            })

        pageData = BaseView.parasePage(int(pageIndex), int(pageSize),
                                       paginator.page(pageIndex).paginator.num_pages,
                                       paginator.count, resl)

        return BaseView.successData(pageData)

    # 添加学生信息
    @transaction.atomic
    def addInfo(request):

        if models.Users.objects.filter(userName=request.POST.get('userName')).exists():
            return BaseView.warn('账号已存在，请重新输入')
        elif models.Users.objects.filter(id=request.POST.get('id')).exists():
            return BaseView.warn('学号已存在，请重新输入')
        else:
            user = models.Users.objects.create(
                id=request.POST.get('id'),
                userName=request.POST.get('userName'),
                passWord=request.POST.get('userName'),
                name=request.POST.get('name'),
                gender=request.POST.get('gender'),
                age=request.POST.get('age'),
                type=2,
            )
            models.Students.objects.create(
                user=user,
                grade=models.Grades.objects.get(id=request.POST.get('gradeId')),
                college=models.Colleges.objects.get(id=request.POST.get('collegeId')),
                status=0
            )
            return BaseView.success()

    # 修改学生信息
    def updInfo(request):

        models.Students.objects. \
            filter(user__id=request.POST.get('id')).update(
                grade=models.Grades.objects.get(id=request.POST.get('gradeId')),
                college=models.Colleges.objects.get(id=request.POST.get('collegeId'))
        )
        return BaseView.success()

    #删除学生信息
    @transaction.atomic
    def delInfo(request):

        if (models.CheckLogs.objects.filter(student__id=request.POST.get('id')).exists() |
                models.LeaveLogs.objects.filter(student__id=request.POST.get('id')).exists()):
            return BaseView.warn('存在关联记录无法移除')
        else:
            models.Users.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()

'''
教师信息处理
'''
class TeachersView(BaseView):

    def get(self, request, module, *args, **kwargs):
        if module == 'page':
            return TeachersView.getPageInfos(request)
        else:
            return BaseView.error('请求地址不存在')

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return TeachersView.addInfo(request)
        elif module == 'upd':
            return TeachersView.updInfo(request)
        elif module == 'del':
            return TeachersView.delInfo(request)
        else:
            return BaseView.error('请求地址不存在')

    # 分页查询教师信息
    def getPageInfos(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')
        record = request.GET.get('record')
        phone = request.GET.get('phone')

        qruery = Q();
        if SysUtil.isExit(name):
            qruery = qruery & Q(user__name__contains=name)
        if SysUtil.isExit(record):
            qruery = qruery & Q(record=record)
        if SysUtil.isExit(phone):
            qruery = qruery & Q(phone__contains=phone)

        data = models.Teachers.objects.filter(qruery)

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            resl.append({
                'id': item.user.id,
                'userName': item.user.userName,
                'name': item.user.name,
                'gender': item.user.gender,
                'age': item.user.age,
                'phone': item.phone,
                'record': item.record
            })

        pageData = BaseView.parasePage(int(pageIndex), int(pageSize),
                                       paginator.page(pageIndex).paginator.num_pages,
                                       paginator.count, resl)

        return BaseView.successData(pageData)

    # 添加教师信息
    @transaction.atomic
    def addInfo(request):

        if models.Users.objects.filter(userName=request.POST.get('userName')).exists():
            return BaseView.warn('账号已存在，请重新输入')
        elif models.Users.objects.filter(id=request.POST.get('id')).exists():
            return BaseView.warn('工号已存在，请重新输入')
        else:
            user = models.Users.objects.create(
                id=request.POST.get('id'),
                userName=request.POST.get('userName'),
                passWord=request.POST.get('userName'),
                name=request.POST.get('name'),
                gender=request.POST.get('gender'),
                age=request.POST.get('age'),
                type=1,
            )
            models.Teachers.objects.create(
                user=user,
                phone=request.POST.get('phone'),
                record=request.POST.get('record')
            )
            return BaseView.success()

    # 修改教师信息
    def updInfo(request):

        models.Teachers.objects. \
            filter(user__id=request.POST.get('id')).update(
            phone=request.POST.get('phone'),
            record=request.POST.get('record')
        )
        return BaseView.success()

    #删除教师信息
    @transaction.atomic
    def delInfo(request):

        if (models.Works.objects.filter(teacher__id=request.POST.get('id')).exists() |
                models.Checks.objects.filter(teacher__id=request.POST.get('id')).exists() |
                models.LeaveLogs.objects.filter(teacher__id=request.POST.get('id')).exists()):
            return BaseView.warn('存在关联记录无法移除')
        else:
            models.Users.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()

'''
教师工作安排
'''
class WorksView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'worklist':
            return WorksView.getWorkInfos(request)
        elif module == 'teaworklist':
            return WorksView.getTeacherWork(request)
        elif module == 'setworklist':
            return WorksView.getSetWorkInfos(request)
        elif module == 'stuworklist':
            return WorksView.getStuWorkInfos(request)
        else:
            return BaseView.error('请求地址不存在')

    def post(self, request, module, *args, **kwargs):

        if module == 'setwork':
            return WorksView.setWork(request)
        else:
            return BaseView.error('请求地址不存在')

    # 获取授课安排信息
    def getWorkInfos(request):

        works = models.Works.objects.filter(grade__id=request.GET.get('gradeId'))

        resl = []
        for item in list(works):

            resl.append({
                'id': item.id,
                'job': item.job,
                'projectId': item.project.id,
                'projectName': item.project.name,
                'gradeId': item.grade.id,
                'gradeName': item.grade.name,
                'teacherId': item.teacher.user.id,
                'teacherName': item.teacher.user.name,
                'teacherAge': item.teacher.user.age,
                'teacherGender': item.teacher.user.gender,
            })

        return BaseView.successData(resl)

    # 获取教师工作
    def getTeacherWork(request):

        works = models.Works.objects.filter(teacher__user__id=request.GET.get('teacherId'))

        resl = []
        for item in list(works):

            resl.append({
                'id': item.id,
                'job': item.job,
                'projectId': item.project.id,
                'projectName': item.project.name,
                'gradeId': item.grade.id,
                'gradeName': item.grade.name,
                'teacherId': item.teacher.user.id,
                'teacherName': item.teacher.user.name,
                'teacherAge': item.teacher.user.age,
                'teacherGender': item.teacher.user.gender,
            })

        return BaseView.successData(resl)

    # 获取授课设置列表
    def getSetWorkInfos(request):

        grade = models.Grades.objects.filter(id=request.GET.get('gradeId')).first()

        print(grade)

        projects = models.Projects.objects.all()

        resl = []

        for item in projects:

            qruery = Q(grade__id=request.GET.get('gradeId'))
            qruery = qruery & Q(project__id=item.id)
            temp = models.Works.objects.filter(qruery)
            if temp.exists():

                temp = temp.first()
                resl.append({
                    'id': temp.id,
                    'job': temp.job,
                    'projectId': item.id,
                    'projectName': item.name,
                    'gradeId': grade.id,
                    'gradeName': grade.name,
                    'teacherId': temp.teacher.user.id,
                    'teacherName': temp.teacher.user.name,
                    'teacherAge': temp.teacher.user.age,
                    'teacherGender': temp.teacher.user.gender,
                    'isSetWork': True
                })
            else:

                resl.append({
                    'id': '',
                    'job': 2,
                    'projectId': item.id,
                    'projectName': item.name,
                    'gradeId': grade.id,
                    'gradeName': grade.name,
                    'teacherId': '',
                    'teacherName': '',
                    'teacherAge': '',
                    'teacherGender': '',
                    'isSetWork': False
                })

        return BaseView.successData(resl)

    # 获取指定学生相关的课程列表
    def getStuWorkInfos(request):

        works = models.Works.objects.filter(grade__id=request.GET.get('gradeId'))

        resl = []
        for item in list(works):
            resl.append({
                'id': item.id,
                'job': item.job,
                'projectId': item.project.id,
                'projectName': item.project.name,
                'gradeId': item.grade.id,
                'gradeName': item.grade.name,
                'teacherId': item.teacher.user.id,
                'teacherName': item.teacher.user.name,
                'teacherPhone': item.teacher.phone,
                'teacherRecord': item.teacher.record,
            })

        return BaseView.successData(resl)

    # 教师工作设置
    def setWork(request):

        qruery = Q(grade__id=request.POST.get('gradeId'))
        qruery = qruery & Q(project__id=request.POST.get('projectId'))
        temp = models.Works.objects.filter(qruery)
        if temp.exists():
            temp.delete()

        if int(request.POST.get('job')) == 1:

            works = models.Works.objects.filter(grade__id=request.POST.get('gradeId'))

            if works.exists():
                works.update(job=0)


        models.Works.objects.create(
            teacher=models.Teachers.objects.get(user__id=request.POST.get('teacherId')),
            project=models.Projects.objects.get(id=request.POST.get('projectId')),
            grade=models.Grades.objects.get(id=request.POST.get('gradeId')),
            job=request.POST.get('job'),
        )

        return BaseView.success()

'''
考勤处理
'''
class ChecksView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module=='page':
            return ChecksView.getPageInfos(request)
        else:
            return BaseView.error('请求地址不存在')

    def post(self, request, module, *args, **kwargs):

        if module == 'add':
            return ChecksView.addInfo(request)
        elif module == 'upd':
            return ChecksView.updInfo(request)
        else:
            return BaseView.error('请求地址不存在')

    # 分页查看考勤处理信息
    def getPageInfos(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)

        gradeId = request.GET.get('gradeId')
        teacherId = request.GET.get('teacherId')
        teacherName = request.GET.get('teacherName')

        qruery = Q();

        if SysUtil.isExit(gradeId):
            qruery = qruery & Q(grade__id=gradeId)

        if SysUtil.isExit(teacherId):
            qruery = qruery & Q(teacher__user__id=teacherId)

        if SysUtil.isExit(teacherName):
            qruery = qruery & Q(teacher__user__name__contains=teacherName)

        data = models.Checks.objects.filter(qruery).order_by('-createTime')

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            resl.append({
                'no': item.no,
                'teacherId': item.teacher.user.id,
                'teacherName': item.teacher.user.name,
                'teacherPhone': item.teacher.phone,
                'gradeId': item.grade.id,
                'gradeName': item.grade.name,
                'createTime': item.createTime,
                'status': item.status,
                'total': models.CheckLogs.objects.filter(checks__no=item.no).count()
            })

        pageData = BaseView.parasePage(int(pageIndex), int(pageSize),
                                       paginator.page(pageIndex).paginator.num_pages,
                                       paginator.count, resl)

        return BaseView.successData(pageData)

    # 添加考勤处理
    def addInfo(request):

        qruery = Q(teacher__user__id=request.POST.get('teacherId'))
        qruery = qruery & Q(grade__id=request.POST.get('gradeId'))
        qruery = qruery & Q(status=0)

        if models.Checks.objects.filter(qruery).exists():

            return BaseView.warn('学生正在打卡, 请勿重复操作!')
        else:

            models.Checks.objects.create(
                no=CheckUtil.createNo(),
                teacher=models.Teachers.objects.get(user__id=request.POST.get('teacherId')),
                grade=models.Grades.objects.get(id=request.POST.get('gradeId')),
                createTime=DateUtil.getNowDateTime(),
                status=0
            )
            return BaseView.success()

    def updInfo(request):

        models.Checks.objects. \
            filter(no=request.POST.get('no')).update(
            status=1
        )
        return BaseView.success()



'''
考勤记录
'''
class CheckLogsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module=='referno':

            return CheckLogsView.getCheckListByNo(request)
        elif module=='referstu':

            return CheckLogsView.getCheckListByStuId(request)
        else:

            return BaseView.error('请求地址不存在')

    def post(self, request, module, *args, **kwargs):

        if module == 'add':

            return CheckLogsView.addInfo(request)
        else:

            return BaseView.error('请求地址不存在')

    # 获取指定考勤码相关的考勤记录
    def getCheckListByNo(request):

        checkLogs = models.CheckLogs.objects.filter(checks__no=request.GET.get('checkNo')).order_by('-createTime')

        resl = []
        for item in list(checkLogs):

            resl.append({
                'id': item.id,
                'createTime': item.createTime,
                'checkNo': item.checks.no,
                'studentId': item.student.user.id,
                'studentName': item.student.user.name,
                'gradeId': item.student.grade.id,
                'gradeName': item.student.grade.name,
            })


        return BaseView.successData(resl)

    # 获取指定学生相关的考勤记录
    def getCheckListByStuId(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)

        data = models.CheckLogs.objects.filter(student__user__id=request.GET.get('studentId')).order_by('-createTime')

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):
            resl.append({
                'id': item.id,
                'createTime': item.createTime,
                'checkNo': item.checks.no,
                'teacherName': item.checks.teacher.user.name,
                'gradeId': item.student.grade.id,
                'gradeName': item.student.grade.name,
            })

        pageData = BaseView.parasePage(int(pageIndex), int(pageSize),
                                       paginator.page(pageIndex).paginator.num_pages,
                                       paginator.count, resl)

        return BaseView.successData(pageData)

    # 添加考勤记录
    def addInfo(request):

        check = models.Checks.objects.filter(no=request.POST.get('checkNo')).first()

        if check == None:

            return BaseView.warn('考勤码输入错误')
        elif check.status==1:

            return BaseView.warn('考勤结束')
        else:

            qruery = Q(checks__no=request.POST.get('checkNo'))
            qruery = qruery & Q(student__user__id=request.POST.get('studentId'))

            if models.CheckLogs.objects.filter(qruery).exists():

                return BaseView.warn('您已完成打卡操作')
            else:

                models.CheckLogs.objects.create(
                    checks=models.Checks.objects.get(no=request.POST.get('checkNo')),
                    student=models.Students.objects.get(user__id=request.POST.get('studentId')),
                    createTime=DateUtil.getNowDateTime()
                )
                return BaseView.success()

'''
学生请假处理
'''
class LeaveLogsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module=='page':

            return LeaveLogsView.getPageInfos(request)
        else:

            return BaseView.error("请求地址不存在")

    def post(self, request, module, *args, **kwargs):

        if module=='add':

            return LeaveLogsView.addInfos(request)
        elif module=='upd':

            return LeaveLogsView.updInfo(request)
        else:

            return BaseView.error('请求地址不存在')

    # 分页查询请假信息
    def getPageInfos(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)

        collegeId = request.GET.get('collegeId')
        gradeId = request.GET.get('gradeId')

        teacherId = request.GET.get('teacherId')

        studentId = request.GET.get('studentId')
        studentName = request.GET.get('studentName')

        qruery = Q();

        if SysUtil.isExit(collegeId):
            qruery = qruery & Q(student__college__id=collegeId)

        if SysUtil.isExit(gradeId):
            qruery = qruery & Q(student__grade__id=gradeId)

        if SysUtil.isExit(teacherId):

            temps = []

            works = models.Works.objects.filter(teacher__user__id=teacherId)

            if works.exists():
                for item in works:
                    temps.append(item.grade.id)

                qruery = qruery & (Q(student__grade__id__in=temps) | Q(teacher__user__id=teacherId))
            else:

                qruery = qruery & Q(teacher__user__id=teacherId)


        if SysUtil.isExit(studentId):
            qruery = qruery & Q(student__user__id=studentId)

        if SysUtil.isExit(studentName):
            qruery = qruery & Q(student__user__name__contains=studentName)

        data = models.LeaveLogs.objects.filter(qruery).order_by('-createTime')

        paginator = Paginator(data, pageSize)

        resl = []

        for item in list(paginator.page(pageIndex)):

            temp_t = item.teacher
            temp_s = item.student

            qruery_1 = Q()
            isAdmin = False
            if SysUtil.isExit(teacherId):
                qruery_1 = qruery_1 & Q(teacher__user__id=teacherId)
                qruery_1 = qruery_1 & Q(grade__id=item.student.grade.id)
                qruery_1 = qruery_1 & Q(job=1)
                isAdmin = models.Works.objects.filter(qruery_1).exists()

            resl.append({
                'id': item.id,
                'reason': item.reason,
                'studentId': item.student.user.id,
                'studentName': item.student.user.name,
                'collegeId': item.student.college.id,
                'collegeName': item.student.college.name,
                'gradeId': item.student.grade.id,
                'gradeName': item.student.grade.name,
                'createTime': item.createTime,
                'teacherId': '' if item.status==0 else item.teacher.user.id,
                'teacherName': '' if item.status==0 else item.teacher.user.name,
                'teacherPhone': '' if item.status==0 else item.teacher.phone,
                'replyTime': '' if item.status==0 else item.replyTime,
                'replyComm': '' if item.status==0 else item.replyComm,
                'status': item.status,
                'isAdmin': isAdmin
            })

        pageData = BaseView.parasePage(int(pageIndex), int(pageSize),
                                       paginator.page(pageIndex).paginator.num_pages,
                                       paginator.count, resl)

        return BaseView.successData(pageData)

    # 添加请假信息
    def addInfos(request):

        student = models.Students.objects.filter(user__id=request.POST.get('studentId')).first()

        if student.status==1:

            return BaseView.warn("休假学员无法执行此操作")
        else:

            qruery = Q(status=0)
            qruery = qruery & Q(student__user__id=request.POST.get('studentId'))

            if models.LeaveLogs.objects.filter(qruery).exists():

                return BaseView.warn('申请审核中，请耐心等待')
            else:

                models.LeaveLogs.objects.create(
                    reason=request.POST.get('reason'),
                    student=models.Students.objects.get(user__id=request.POST.get('studentId')),
                    createTime=DateUtil.getNowDateTime("%Y-%m-%d"),
                    status=0
                )
                return BaseView.success()

    # 修改请求信息
    @transaction.atomic
    def updInfo(request):

        status = int(request.POST.get('status'))

        if status==1:

            models.LeaveLogs.objects. \
                filter(id=request.POST.get('id')).update(
                teacher=models.Teachers.objects.get(user__id=request.POST.get('teacherId')),
                replyComm=request.POST.get('replyComm'),
                replyTime=DateUtil.getNowDateTime(),
                status=1
            )
            models.Students.objects. \
                filter(user__id=request.POST.get('stuId')).update(
                status=1
            )
            return BaseView.success()
        elif status==2:

            models.LeaveLogs.objects. \
                filter(id=request.POST.get('id')).update(
                teacher=models.Teachers.objects.get(user__id=request.POST.get('teacherId')),
                replyComm=request.POST.get('replyComm'),
                replyTime=DateUtil.getNowDateTime(),
                status=2
            )
            return BaseView.success()
        elif status==3:

            models.LeaveLogs.objects. \
                filter(id=request.POST.get('id')).update(
                status=3
            )
            models.Students.objects. \
                filter(user__id=request.POST.get('stuId')).update(
                status=0
            )
            return BaseView.success()
















