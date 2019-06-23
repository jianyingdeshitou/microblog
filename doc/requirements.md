# 项目所需组件

## Flask==1.0.2

(略)

## Flask-WTF==0.14.2

这是一个围绕WTForms包的薄包装，可以很好地将它与Flask集成。

## Flask-SQLAlchemy==2.4.0

关于SQLAlchemy的好处是它不是一个ORM，而是许多关系数据库。SQLAlchemy支持一长串数据库引擎，包括流行的MySQL，PostgreSQL和SQLite。这非常强大，因为您可以使用不需要服务器的简单SQLite数据库进行开发，然后在生产服务器上部署应用程序时，您可以选择更强大的MySQL或PostgreSQL服务器，而无需改变你的申请。

## Flask-Migrate==2.5.2

此扩展是Alembic的Flask包装器，它是SQLAlchemy的数据库迁移框架。使用数据库迁移为启动数据库添加了一些工作，但这是一个很小的代价，可以为将来对数据库进行更改提供强大的方法。

## PyMySQL==0.9.3

PyMySQL 是在 Python3.x 版本中用于连接 MySQL 服务器的一个库，Python2中则使用mysqldb。

PyMySQL 遵循 Python 数据库 API v2.0 规范，并包含了 pure-Python MySQL 客户端库。

未安装，使用时会遇到：ModuleNotFoundError: No module named 'MySQLdb'

## python-dotenv==0.10.3

由于不会在终端会话中记住FLASK_APP环境变量，因此在打开新的终端窗口时，您可能总是需要设置环境变量。从版本1.0开始，Flask允许您注册在运行flask命令时要自动导入的环境变量。要使用此选项，您必须安装python-dotenv包：

然后，您可以在项目的顶级目录中的.flaskenv文件中编写环境变量名称和值：

.flaskenv：flask命令的环境变量

```
FLASK_APP=microblog.py
```


