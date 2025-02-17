## 使用方法


## 安装方法

### Windows 部署
1.从[发行版本](https://github.com/PIKACHUIM/StunConnects/releases)下载二进制文件
2.启动`StunConnects.exe`即可

### Android 部署
1.从[发行版本](https://github.com/PIKACHUIM/StunConnects/releases)下载二进制文件
2.安装APK，然后启动`StunConnects`即可

### LinuxOS 部署
1.从[发行版本](https://github.com/PIKACHUIM/StunConnects/releases)下载二进制文件
2.启动`StunConnects.appImage`即可

### Dockerd 部署

#### 直接启动

使用下列命令启动docker容器

```shell
docker run -d --network host --name porter-container pikachuim/porter:latest
```

然后您可以通过`ip:1680`访问您的管理页面，您可能需要放行防火墙

#### 使用模板

创建一个`docker-compose.yml`

```yaml
version: '3.8'  # Docker Compose 版本
services:
  porter-container: # 定义服务名称
    image: pikachuim/porter:latest  # 使用的镜像
    container_name: porter-container  # 容器名称
    network_mode: host  # 使用 Host 网络模式
    restart: unless-stopped  # 重启策略
```

然后启动docker：

```shell
docker-compose up -d
```

## 可选参数

### 隐藏窗口

不会显示窗口，静默启动程序
```shell
StunConnects.exe --hide-window
```

### 服务模式
非交互式启动，无头服务器用
```shell
StunConnects.exe --flag-server
```

## 使用方法
详见：[使用方法](https://github.com/PIKACHUIM/StunConnects/blob/main/USAGES.MD)