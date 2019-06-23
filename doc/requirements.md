# 项目所需组件

## Flask==1.0.2

(略)

## python-dotenv==0.10.3

由于不会在终端会话中记住FLASK_APP环境变量，因此在打开新的终端窗口时，您可能总是需要设置环境变量。从版本1.0开始，Flask允许您注册在运行flask命令时要自动导入的环境变量。要使用此选项，您必须安装python-dotenv包：

然后，您可以在项目的顶级目录中的.flaskenv文件中编写环境变量名称和值：

.flaskenv：flask命令的环境变量

```
FLASK_APP=microblog.py
```


