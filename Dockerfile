FROM python:3.7

# 设置工作目录
RUN mkdir -p /src
WORKDIR /src

ADD ./requirements.txt /src/requirements.txt

# 安装依赖
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 添加应用
ADD . /src

EXPOSE 5000

ENV FLASK_APP=app.py

# 运行服务
CMD python -m flask run --host=0.0.0.0
