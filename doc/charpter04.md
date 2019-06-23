# 第4章：数据库

## 播放时间

进入Python提示后，让我们导入数据库实例和模型：

```python
>>> from app import db
>>> from app.models import User, Post
```

首先创建一个新用户：

```python
>>> u = User(username='john', email='john@example.com')
>>> db.session.add(u)
>>> db.session.commit()
```

对数据库的更改在会话的上下文中完成，可以作为db.session。可以在会话中累积多个更改，并且一旦注册了所有更改，您就可以发出单个db.session.commit()更改，以原子方式写入所有更改。如果在会话期间的任何时间都有错误，则调用db.session.rollback()将中止会话并删除存储在其中的任何更改。要记住的重要一点是，只有在db.session.commit()调用时才会将更改写入数据库。会话保证数据库永远不会处于不一致状态。

让我们添加另一个用户：

```python
>>> u = User(username='susan', email='susan@example.com')
>>> db.session.add(u)
>>> db.session.commit()
```

数据库可以回答返回所有用户的查询：

```python
>>> users = User.query.all()
>>> users
[<User john>, <User susan>]
>>> for u in users:
...     print(u.id, u.username)
...
1 john
2 susan
```

所有模型都有一个query属性，它是运行数据库查询的入口点。最基本的查询是返回该类的所有元素，该类被适当地命名all()。请注意，id添加这些用户时，字段会自动设置为1和2。

这是另一种进行查询的方法。如果您知道id用户的身份，则可以按如下方式检索该用户：

```python
>>> u = User.query.get(1)
>>> u
<User john>
```

现在让我们添加一篇博文：

```python
>>> u = User.query.get(1)
>>> p = Post(body='my first post!', author=u)
>>> db.session.add(p)
>>> db.session.commit()
```

我不需要为该timestamp字段设置值，因为该字段具有默认值，您可以在模型定义中看到该值。那user_id场呢？回想一下，db.relationship我在User类中创建的posts属性为用户添加了属性，并author为帖子添加了属性。我使用author虚拟字段将作者分配到帖子，而不是必须处理用户ID。SQLAlchemy在这方面非常出色，因为它提供了对关系和外键的高级抽象。

要完成此会话，我们来看几个数据库查询：

```python
>>> # get all posts written by a user
>>> u = User.query.get(1)
>>> u
<User john>
>>> posts = u.posts.all()
>>> posts
[<Post my first post!>]

>>> # same, but with a user that has no posts
>>> u = User.query.get(2)
>>> u
<User susan>
>>> u.posts.all()
[]

>>> # print post author and body for all posts
>>> posts = Post.query.all()
>>> for p in posts:
...     print(p.id, p.author.username, p.body)
...
1 john my first post!

# get all users in reverse alphabetical order
>>> User.query.order_by(User.username.desc()).all()
[<User susan>, <User john>]
```

Flask-SQLAlchemy的文档，了解可用来查询数据库中的许多选项的最佳场所。

要完成此部分，让我们删除上面创建的测试用户和帖子，以便数据库干净并为下一章做好准备：

```python
>>> users = User.query.all()
>>> for u in users:
...     db.session.delete(u)
...
>>> posts = Post.query.all()
>>> for p in posts:
...     db.session.delete(p)
...
>>> db.session.commit()
```

## Shell上下文

microblog.py中的以下函数创建一个shell上下文，将数据库实例和模型添加到shell会话中：

```python
from app import app, db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
```

所述app.shell_context_processor装饰注册功能作为壳上下文功能。当flask shell命令运行时，它将调用此函数并在shell会话中注册它返回的项。函数返回字典而不是列表的原因是，对于每个项目，您还必须提供一个名称，在该名称下将在shell中引用它，这由字典键给出。

添加shell上下文处理器功能后，您可以使用数据库实体而无需导入它们：

```python
(venv) $ flask shell
>>> db
<SQLAlchemy engine=sqlite:////Users/migu7781/Documents/dev/flask/microblog2/app.db>
>>> User
<class 'app.models.User'>
>>> Post
<class 'app.models.Post'>
```

如果你尝试了上面并获得NameError当你访问异常db，User以及Post，那么make_shell_context()函数没有被用瓶注册。最可能的原因是您尚未设置FLASK_APP=microblog.py环境。在这种情况下，请返回第1章并查看如何设置FLASK_APP环境变量。如果您在打开新的终端窗口时经常忘记设置此变量，则可以考虑将.flaskenv文件添加到项目中，如该章末尾所述。
