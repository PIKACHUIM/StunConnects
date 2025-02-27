FROM python:3.12-slim

# 安装 Flet
RUN pip install flet

# 将你的 Python 文件复制到容器中
COPY src/StunConnects.ico /app/StunConnects.ico
COPY src/pipConfigure.txt /app/pipConfigure.txt
COPY src/StunConnects.py  /app/StunConnects.py

COPY src/StunDesktops.py  /app/StunDesktops.py
COPY src/assets           /app/assets/
COPY src/config           /app/config/
COPY src/module           /app/module/
COPY src/main.py          /app/main.py
RUN  pip install -r       /app/pipConfigure.txt

# 设置工作目录
WORKDIR /app

# 启动 Flet 应用
CMD ["python", "main.py", "--flag-server"]