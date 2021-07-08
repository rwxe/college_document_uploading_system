import django
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404, StreamingHttpResponse, FileResponse
from django.utils import timezone
from django.db.utils import DataError
from django.urls import reverse
from django.contrib.auth import hashers
from django.core import mail, cache
from django.db.models import Q
from . import models
import random
import string
import datetime
import random
from django.conf import settings
import sys

# Create your views here.


def hint_and_redirect(request, the_url, hint, show_hint=True, delay_time=1000):
    if show_hint == False:
        return redirect(the_url)
    else:
        context = {'the_url': the_url,
                   'hint': hint,
                   'delay_time': delay_time,
                   }
        return render(request, 'cdus/hint.html', context)


def index(request):
    context = {
    }
    return render(request, 'cdus/index.html', context)


def console(request, user_type):
    # 主要的交互界面
    if request.method == 'GET':
        commit_list = []
        if user_type == 'teacher':
            user = get_object_or_404(
                models.Teacher, id=request.session.get('id'))

            # 先遍历这个老师教的所有课
            for tc in user.teachingcourse_set.all():
                # 再遍历这个老师教的这个课的班级
                for ctc in tc.clazzteachingcourse_set.all():
                    try:
                        ctc.unrevieweddoc
                        print(ctc, "有")
                        commit_list.append(
                            {"ctc_name": ctc.__str__(), "ctc_id": ctc.id, "status": ctc.unrevieweddoc.status})
                    except:
                        print(ctc, "无")
                        commit_list.append(
                            {"ctc_name": ctc.__str__(), "ctc_id": ctc.id, "status": "未提交"})
            context = {
                'commit_list': commit_list,
            }
            return render(request, 'cdus/teacher_console.html', context)

        elif user_type == 'approver':
            user = get_object_or_404(
                models.Approver, id=request.session.get('id'))
            for ud in models.UnreviewedDoc.objects.all().order_by('-id'):
                commit_list.append(
                       {"ud_name": ud.__str__(), "ud_id": ud.id, "status": ud.status,"files":get_file_context(ud.id)})

            context = {
                'commit_list': commit_list,
            }
            return render(request, 'cdus/approver_console.html', context)
        else:
            return hint_and_redirect(request, reverse('cdus:index'), '未知的用户类型', True)


def post_doc(request: HttpRequest, ctc_id):

    if request.method == 'GET':
        context = {}
        return render(request, 'cdus/post_doc.html', context)
    elif request.method == 'POST':
        try:
            unreviewed_doc = models.UnreviewedDoc.objects.get(
                clazz_teaching_course=models.ClazzTeachingCourse.objects.get(pk=ctc_id))
        except models.UnreviewedDoc.DoesNotExist:
            unreviewed_doc = models.UnreviewedDoc()

        print(repr(request.POST.get('is_open')))
        print(repr(request.POST.get('num_of_test_paper')))

        unreviewed_doc.clazz_teaching_course = models.ClazzTeachingCourse.objects.get(
            pk=ctc_id)
        unreviewed_doc.status = '未审核'
        unreviewed_doc.transcripts = request.FILES.get('transcripts')
        unreviewed_doc.regular_grade = request.FILES.get('regular_grade')
        unreviewed_doc.answer = request.FILES.get('answer')
        unreviewed_doc.exam_analysis = request.FILES.get('exam_analysis')
        unreviewed_doc.work_summary = request.FILES.get('work_summary')
        unreviewed_doc.num_of_test_paper = int(
            request.POST.get('num_of_test_paper'))
        if request.POST.get('is_open') == 'on':
            unreviewed_doc.is_open = True
        else:
            unreviewed_doc.is_open = False

        unreviewed_doc.save()
        return hint_and_redirect(request, reverse('cdus:console', args=["teacher"]), '上传成功了', False)


def get_file_context(ud_id):
    files = []
    ud = models.UnreviewedDoc.objects.get(pk=ud_id)

    if len(ud.transcripts.name) != 0:
        files.append({"name": "成绩单", "url": ud.transcripts.url})
    if len(ud.regular_grade.name) != 0:
      files.append({"name": "平时成绩", "url": ud.regular_grade.url})
    if len(ud.answer.name) != 0:
      files.append({"name": "答案", "url": ud.answer.url})
    if len(ud.exam_analysis.name) != 0:
      files.append({"name": "试卷分析", "url": ud.exam_analysis.url})
    if len(ud.work_summary.name) != 0:
        files.append({"name": "工作总结", "url": ud.work_summary.url})

    print(files)
    if ud.is_open:
        files.append({"name": "开卷", "url": ""})
    else:
        files.append({"name": "闭卷", "url": ""})

    files.append({"name": "试卷本数:"+str(ud.num_of_test_paper), "url": ""})

    return files


def review(request, ud_id, op):
    ud = models.UnreviewedDoc.objects.get(pk=ud_id)
    ctc = ud.clazz_teaching_course
    if op == 'pass':
        ud.status = '已通过'
        try:
            rd = models.ReviewedDoc.objects.get(clazz_teaching_course=ctc)
        except:
            rd = models.ReviewedDoc()
        finally:
            rd.clazz_teaching_course = ctc
            rd.transcripts = ud.transcripts
            rd.regular_grade = ud.regular_grade
            rd.answer = ud.answer
            rd.exam_analysis = ud.exam_analysis
            rd.work_summary = ud.work_summary
            rd.num_of_test_paper = ud.num_of_test_paper
            rd.is_open = ud.is_open
            rd.save()
            # 同时修改unreviewed_doc的状态
            ud.save()
    elif op == 'fail':
        ud.status = '未通过'
        ud.save()

    return hint_and_redirect(request, reverse('cdus:console', args=["approver"]), '审批成功了', True)


def qft(request):
    files = []
    ud = models.UnreviewedDoc.objects.get(pk=4)

    if len(ud.transcripts.name) != 0:
        files.append({"name": "成绩单", "url": ud.transcripts.url})
    if len(ud.regular_grade.name) != 0:
      files.append({"name": "平时成绩", "url": ud.regular_grade.url})
    if len(ud.answer.name) != 0:
      files.append({"name": "答案", "url": ud.answer.url})
    if len(ud.exam_analysis.name) != 0:
      files.append({"name": "试卷分析", "url": ud.exam_analysis.url})
    if len(ud.work_summary.name) != 0:
        files.append({"name": "工作总结", "url": ud.work_summary.url})

    print(files)
    if ud.is_open:
        is_open = "开卷"
    else:
        is_open = "闭卷"

    context = {'files': files,
               'is_open': is_open,
               'num_of_test_paper': ud.num_of_test_paper,
               }
    return render(request, 'cdus/qft.html', context)
    # return HttpResponse('<a href="'+rd.transcripts.url+'">s</a>')
    # return FileResponse(rd.transcripts,as_attachment=True)
    # return StreamingHttpResponse(rd.transcripts.chunks())



def login(request, user_type):
    # 转换成小写，确保下面比对不会出问题
    user_type = user_type.lower()

    if request.method == 'GET':
        if user_type == 'teacher':
            the_type = '教师'
        elif user_type == 'approver':
            the_type = '审批人'
        else:
            return hint_and_redirect(request, reverse('cdus:index'), '未知的用户类型', True)

        context = {
            'user_type': the_type
        }
        return render(request, 'cdus/login.html', context)

    elif request.method == 'POST':
        email = request.POST.get('email')
        p1 = request.POST.get('password1')

        try:
            # 判别用户类型
            if user_type == 'teacher':
                result = models.Teacher.objects.get(email=email)
            elif user_type == 'approver':
                result = models.Approver.objects.get(email=email)
            else:
                print("BUG,不知道这是什么用户类型")
                return HttpResponse("我不知道这是什么用户类型")

            if hashers.check_password(p1, result.password):
                request.session['name'] = result.name
                request.session['id'] = result.id
                request.session['user_type'] = user_type
                return hint_and_redirect(request, reverse('cdus:console', args=[user_type]), '登录成功了', False)

            else:
                context = {'err_msg': '密码错误',
                           }
                return render(request, 'cdus/login.html', context)

        except models.Teacher.DoesNotExist:
            context = {'err_msg': '此用户不存在',
                       }
            return render(request, 'cdus/login.html', context)
        except models.Approver.DoesNotExist:
            context = {'err_msg': '此用户不存在',
                       }
            return render(request, 'cdus/login.html', context)
        except:
            ex_type, ex_val, ex_stack = sys.exc_info()
            print(sys.exc_info())
            return HttpResponse("出BUG了")
    else:
        return HttpResponse("出BUG了")


def register(request, user_type):
    # 注册页面
    print(user_type)
    if request.method == 'GET':
        colleges = models.College.objects.all()
        if user_type == 'teacher' or user_type=='教师':
            the_type = '教师'
        elif user_type == 'approver' or user_type=='审批人':
            the_type = '审批人'
        else:
            return hint_and_redirect(request, reverse('cdus:index'), '未知的用户类型', True)

        context = {'err_msg': '',
                   'colleges': colleges,
                   'user_type': the_type
                   }
        return render(request, 'cdus/register.html', context)
    elif request.method == 'POST':

        name = request.POST.get('name')
        # 邮箱也要检测是否唯一
        email = request.POST.get('email')
        college_id = request.POST.get('college')
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')

        if user_type == 'teacher':
            new_user = models.Teacher()
            new_user.college = models.College.objects.get(pk=college_id)
            TYPE_USER = models.Teacher
        elif user_type == 'approver':
            new_user = models.Approver()
            new_user.college = models.College.objects.get(pk=college_id)
            TYPE_USER = models.Approver
        else:
            print("BUG,不知道这是什么用户类型")
            return HttpResponse("我不知道这是什么用户类型")

        try:
            # 检测数据库中是否已存在同名用户，若抛出该用户
            # 名不存在异常，则为可以存入数据库

            TYPE_USER.objects.get(name=name)
            context = {'err_msg': '此用户名已存在，请更换一个',
                       }
            return render(request, 'cdus/register.html', context)
        except TYPE_USER.DoesNotExist:
            new_user.name = name

        try:
            # 检测数据库中是否已存在相同邮箱，若抛出该邮箱
            # 不存在异常，则为可以存入数据库
            TYPE_USER.objects.get(email=email)
            context = {'err_msg': '此邮箱已存在，请更换一个',
                       }
            return render(request, 'cdus/register.html', context)
        except TYPE_USER.DoesNotExist:
            new_user.email = email

        if p1 != p2:
            context = {'err_msg': '两次输入的密码不同，请检查是否有误',
                       }
            return render(request, 'cdus/register.html', context)
        else:
            p1_encrypted = hashers.make_password(p1, None, 'pbkdf2_sha256')
            new_user.password = p1_encrypted
            try:
                new_user.save()
                return hint_and_redirect(request, reverse('cdus:index'), '注册成功了')

            except DataError:
                context = {'err_msg': '数据错误，请检查您输入的内容是否符合格式',
                           }
                return render(request, 'cdus/register.html', context)
            except:
                ex_type, ex_val, ex_stack = sys.exc_info()
                print(sys.exc_info())
                return HttpResponse("出BUG了")


def logout(request):
    if 'name' in request.session:
        print('删掉了session')
        request.session.flush()
    return hint_and_redirect(request, reverse('cdus:index'), '登出成功了', False)
