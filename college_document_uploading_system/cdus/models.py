from django.db import models
from django.utils import timezone


class College(models.Model):
    # 学院
    # id 自动创建
    name = models.CharField(max_length=20,  verbose_name='学院名')

    def __str__(self):
        return self.name


class Major(models.Model):
    # 专业
    # id 自动创建
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, verbose_name='所属学院')
    name = models.CharField(max_length=20,  verbose_name='专业名')

    def __str__(self):
        return self.name


class Teacher(models.Model):
    # 任课老师
    # id 自动创建
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, verbose_name='所属学院')
    name = models.CharField(max_length=20,  verbose_name='教师名')
    email = models.CharField(max_length=100,unique=True, verbose_name='邮箱')
    password = models.CharField(max_length=100, verbose_name='密码字段')

    def __str__(self):
        return self.name


class Course(models.Model):
    # 课程
    # id 自动创建
    # 课程并不关联到一个学院上，具体这样做是不是对的，我也不知道
    name = models.CharField(max_length=20,  verbose_name='课程名')
    # 为了简便开发，课程没有学分字段

    def __str__(self):
        return self.name


class Clazz(models.Model):
    # 班级，叫Clazz是为了避免歧义
    # id 自动创建
    major = models.ForeignKey(
        Major, on_delete=models.CASCADE, verbose_name='所学专业')
    grade = models.CharField(max_length=20,  verbose_name='年级')
    name = models.CharField(max_length=20,  verbose_name='班级名称')

    def __str__(self):
        return self.name


class TeachingCourse(models.Model):
    # 讲授课，也就是开设了的课程
    # id 自动创建
    term = models.CharField(max_length=20,  verbose_name='开设学期')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='课程')
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, verbose_name='授课老师')

    def __str__(self):
        return self.term+' '+self.course.name+' '+self.teacher.name
    # 没有教室字段


class ClazzTeachingCourse(models.Model):
    # 班级课程表，也就是，哪个班要上哪个课
    # id 自动创建
    clazz = models.ForeignKey(
        Clazz, on_delete=models.CASCADE, verbose_name='班级')
    teaching_course = models.ForeignKey(
        TeachingCourse, on_delete=models.CASCADE, verbose_name='课程')

    def __str__(self):
        return self.clazz.name+' '+self.teaching_course.__str__()


class UnreviewedDoc(models.Model):
    # 待审核教学文件
    # 待审核的教学文件，不会长期存在于数据库中，当一个班级讲授课存在一个
    # 对应的待审核的教学文件。再次上传将会被覆盖。
    # 如果审批状态发生了变化，该条记录会被删除



    # id 自动创建

    clazz_teaching_course = models.OneToOneField(
        ClazzTeachingCourse, on_delete=models.CASCADE, verbose_name='所属班级课程')
    status = models.CharField(max_length=20,  verbose_name='审批状态')
    # 下面是各种教学文件，采用Django文件字段储存
    # transcripts 成绩单
    transcripts = models.FileField(verbose_name='成绩单')
    # regular_grade 平时成绩
    regular_grade = models.FileField(verbose_name='平时成绩')
    # answer 答案
    answer = models.FileField(verbose_name='答案')
    # exam_analysis 试卷分析
    exam_analysis = models.FileField(verbose_name='试卷分析')
    # work_summary 工作总结
    work_summary = models.FileField(verbose_name='工作总结')
    # num_of_test_paper 试卷本数
    num_of_test_paper = models.IntegerField(verbose_name='试卷本数')
    # is_open 是否开卷
    is_open = models.BooleanField(verbose_name='是否开卷')

    def __str__(self):
        return self.clazz_teaching_course.__str__()+' '+self.status


class ReviewedDoc(models.Model):
    # id 自动生成
    # 这个模型和上面是一样的，但是数据会被永久保存

    clazz_teaching_course = models.OneToOneField(
        ClazzTeachingCourse, on_delete=models.CASCADE, verbose_name='所属班级课程')
    
    # 下面是各种教学文件，采用Django文件字段储存
    # transcripts 成绩单
    transcripts = models.FileField(verbose_name='成绩单')
    # regular_grade 平时成绩
    regular_grade = models.FileField(verbose_name='平时成绩')
    # answer 答案
    answer = models.FileField(verbose_name='答案')
    # exam_analysis 试卷分析
    exam_analysis = models.FileField(verbose_name='试卷分析')
    # work_summary 工作总结
    work_summary = models.FileField(verbose_name='工作总结')
    # num_of_test_paper 试卷本数
    num_of_test_paper = models.IntegerField(verbose_name='试卷本数')
    # is_open 是否开卷
    is_open = models.BooleanField(verbose_name='是否开卷')

    def __str__(self):
        return self.clazz_teaching_course.__str__()
