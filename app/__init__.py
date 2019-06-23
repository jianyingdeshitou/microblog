from flask import Flask

# 小写的“config”是Python模块config.py的名称，
# 显然具有大写“C”的那个是实际的类。
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

from app import routes
