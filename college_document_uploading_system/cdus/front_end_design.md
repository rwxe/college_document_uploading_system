# 主页

**URL** : `index/`

**header**：右边有教师或教务处管理员姓名，点击名字可以进入个人中心或退出

**body**：

教师的主页：

根据这学期他所上的课程，有一个个的课程列表，点击课程，会有个二级菜单，菜单栏目是一个个班级，点击班级，会有一个三级菜单，让他上传一个个文档。

```
+ 课程1

	+ 班级1

		* 上传表单

	+ 班级2

		* 上传表单

- 课程2
```
```json
{
    "所有课程":[
        {
            "课程1":[
                {
                    "班级1":"/the_api/<:id>"
                },
                {
                    "班级2":"/the_api/<:id>"
                }
            ]
        },
        {
            "课程2":[
                {
                    "班级1":"/the_api/<:id>"
                },
                {
                    "班级2":"/the_api/<:id>"
                }
            ]
        }
    ]
}
```



教务处审批员：

和老师界面差不多，但是二级菜单里能看到所有老师的

```
+ 课程1

	+ 班级1（老师1）

		* 下载文件界面
		审批按钮（成功、失败）

	+ 班级2（老师1）
		* 下载文件界面
		审批按钮（成功、失败）
	+ 班级3 （老师2）
		* 下载文件界面
		审批按钮（成功、失败）

- 课程2
```



