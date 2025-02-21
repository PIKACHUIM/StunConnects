FROM python:3.12-slim

# 安装 Flet
RUN pip install flet

# 将你的 Python 文件复制到容器中
COPY StunConnects.ico /app/StunConnects.ico
COPY pipConfigure.txt /app/pipConfigure.txt
COPY StunConnects.py  /app/StunConnects.py
COPY StunServices.py  /app/StunServices.py
COPY appSources       /app/appSources/
COPY subModules       /app/subModules/
RUN  pip install -r   /app/pipConfigure.txt

# 设置工作目录
WORKDIR /app

# 启动 Flet 应用
CMD ["python", "--flag-server", "StunConnects.py"]