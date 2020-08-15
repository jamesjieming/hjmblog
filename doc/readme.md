# 搭建博客踩的坑

### 搭建虚拟环境

PyCharm直接可以创建pipenv环境，但是改了安装源会出问题，安装源在pipfile文件里改

```
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true
```

`pipenv install django==2.2.3`安装django，可以指定版本号。

`pipenv run python manage.py runserver`启动开发服务器。

### 创建工程

```
pipenv run django-admin startproject projectname path
```

`projectname`:工程名

`path`：最后一个参数指定路径，指定已创建的文件夹，否则会在当前文件夹下创建一个新的子文件夹。

### 修改基础设置

`settings.py`文件中修改`LANGUAGE_CODE = 'zh-hans'`,`TIME_ZONE = 'Asia/Shanghai'`

### 创建应用

`pipenv run python manage.py startapp blog`创建blog应用。

在`settings.py`中更改配置

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog', # 注册 blog 应用
]
```

### 创建模型、迁移数据库

在`models.py`中创建模型

`pipenv run python manage.py makemigrations`生成迁移文件

`pipenv run python manage.py migrate`迁移数据库

定义好 `__str__` 方法后，解释器显示的内容将会是 `__str__` 方法返回的内容。

### 配置urls

在应用目录下创建`urls.py`文件在 blog\urls.py 中写入这些代码：

```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

django 匹配 URL 模式是在 工程目录（即 settings.py 文件所在的目录）的 urls.py 下的，所以我们要把 blog 应用下的 urls.py 文件包含到工程目录的urls.py 里去，打开这个文件看到如下内容：

```

"""
一大段注释
"""

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

修改成如下的形式：

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

### 创建模版

## 环境配置

### 安装Nginx

#### centos安装

Install the prerequisites:

> ```
> sudo yum install yum-utils
> ```

To set up the yum repository, create the file named `/etc/yum.repos.d/nginx.repo` with the following contents:

> ```
> [nginx-stable]
> name=nginx stable repo
> baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
> gpgcheck=1
> enabled=1
> gpgkey=https://nginx.org/keys/nginx_signing.key
> module_hotfixes=true
> 
> [nginx-mainline]
> name=nginx mainline repo
> baseurl=http://nginx.org/packages/mainline/centos/$releasever/$basearch/
> gpgcheck=1
> enabled=0
> gpgkey=https://nginx.org/keys/nginx_signing.key
> module_hotfixes=true
> ```

By default, the repository for stable nginx packages is used. If you would like to use mainline nginx packages, run the following command:

> ```
> sudo yum-config-manager --enable nginx-mainline
> ```

To install nginx, run the following command:

> ```
> sudo yum install nginx
> ```

When prompted to accept the GPG key, verify that the fingerprint matches `573B FD6B 3D8F BC64 1079 A6AB ABF5 BD82 7BD9 BF62`, and if so, accept it.

#### Nginx控制

##### 启动Nginx

- nginx [-c configpath]

##### 查看信息

- nginx -v
- nginx -V 

##### 控制Nginx

- nginx -s stop  快速关闭
- nginx -s quit   优雅关闭
- nginx -s reload  重新加载配置

##### 通过系统管理

- systemctl status nginx 查看nginx状态
- systemctl start nginx 启动nginx服务
- systemctl stop nginx 关闭nginx服务
- systemctl enable nginx 设置开机自启
- systemctl disable nginx 禁止开机自启

##### 指令

- nginx -t 不运行，仅测试配置文件
- nginx -c configpath 从指定路径加载配置文件
- nginx -t -c configpath 测试指定配置文件 （指定配置文件使用绝对路径）

##### sever模块配置

- listen 80 指定虚拟主机监听的端口
- server_name_localhost 指定ip地址或域名，多个域名使用空格隔开
- charset utf-8 指定网页的默认编码格式
- error_page 500 502/50x.html 指定错误页面
- access_log xxx main 指定寻主机的访问日志存放的路径
- error_log xxx main 指定寻主机的错误日志存放路径
- root xxx 指定这个寻主机的根目录
- index xxx 指定默认首页

##### location模块配置

sever模块的子模块

location [modifier] url {}

modifier

- =  使用精确匹配并且终止搜索
- ~ 区分大小写的正则表达式
- ~* 不区分大小的正则表达式
- ^~ 最佳匹配，不是正则表达式，通常用来匹配目录

常用指令

- alias 别名

### 安装Gunicorn

首先进入到项目根目录，安装 Gunicorn：

```
yangxg@server:$ pipenv install gunicorn
```

由于我们在服务端修改安装了 gunicorn，代码中 Pipfile 文件和 Pipfile.lock 文件会被更新，因此别忘了把改动同步到本地，具体做法可以自行学习，以下是一个参考：

```
# 服务端提交代码
yangxg@server:$ git add Pipfile Pipfile.lock
yangxg@server:$ git commit -m "add gunicorn dependency"
yangxg@server:$ git push

# 本地拉取代码
git pull
```

回到线上服务器，在项目根目录，执行下面的命令启动服务：

```
yangxg@server:$ pipenv run gunicorn blogproject.wsgi -w 2 -k gthread -b 0.0.0.0:8000
```

来解释一下各个参数的含义。

`-w 2 表示启动 2 个 worker 用于处理请求（一个 worker 可以理解为一个进程），通常将 worker 数目设置为 CPU 核心数的 2-4 倍。

`-k gthread` 指定每个 worker 处理请求的方式，根据大家的实践，指定为 `gthread` 的异步模式能获取比较高的性能，因此我们采用这种模式。

`-b 0.0.0.0:8000`，将服务绑定到 8000 端口，运行通过公网 ip 和 8000 端口访问应用。

### 管理 Gunicorn 进程

现在 Gunicorn 是我们手工启动的，一旦我们退出 shell，服务器就关闭了，博客无法访问。就算在后台启动 Gunicorn，万一哪天服务器崩溃重启了又得重新登录服务器去启动，非常麻烦。为此使用 Supervisor 来管理 Gunicorn 进程，这样当服务器重新启动或者 Gunicorn 进程意外崩溃后，Supervisor 会帮我们自动重启 Gunicorn。

先按 Ctrl + C 停止刚才启动的 Gunicorn 服务进程。

首先安装 Supervisor。注意这里使用的是**系统自带的 pip2**，因为截至本教程书写时 Supervisor 还不支持 Python3，不过这并不影响使用。

```
yangxg@server:$ pip install supervisor
```

为了方便，我一般会设置如下的目录结构（位于 ~/etc 目录下）来管理 Supervisor 有关的文件：

```
~/etc

├── supervisor
│   ├── conf.d
│   └── var
│       ├── log
└── supervisord.conf
```

其中 supervisord.conf 是 Supervior 的配置文件，它会包含 conf.d 下的配置。var 目录下用于存放一些经常变动的文件，例如 socket 文件，pid 文件，log 下则存放日志文件。

首先来建立上述的目录结构：

```
yangxg@server:$ mkdir -p ~/etc/supervisor/conf.d
yangxg@server:$ mkdir -p ~/etc/supervisor/var/log
```

然后进入 ~/etc 目录下生成 Supervisor 的配置文件：

```
yangxg@server:$ cd ~/etc
yangxg@server:$ echo_supervisord_conf > supervisord.conf
```

修改 supervisor.conf，让 Supervisor 进程产生的一些文件生成到上面我们创建的目录下，而不是其默认指定的地方。

首先找到 [unix_http_server] 版块，将 file 设置改为如下的值：

```
[unix_http_server]
file=/home/yangxg/etc/supervisor/var/supervisor.sock
```

即让 socket 文件生成在 ~/etc/supervisor/var/ 目录下。注意 supervisor 不支持将 ~ 展开为用户 home 目录，所以要用绝对路径指定。

类似的修改 [supervisord] 板块下的 logfile 和 pidfile 文件的路径，还有 user 改为系统用户，这样 supervisor 启动的进程将以系统用户运行，避免可能的权限问题：

```
logfile=/home/yangxg/etc/supervisor/var/log/supervisord.log
pidfile=/home/yangxg/etc/supervisor/var/supervisord.pid
user=yangxg
```

还有 [supervisorctl] 板块下：

```
serverurl=unix:///home/yangxg/etc/supervisor/var/supervisor.sock
```

[include] 版块，将 /home/yangxg/etc/supervisor/conf.d/ 目录下所有以 .ini 结尾的文件内容包含到配置中来，这样便于配置的模块化管理，和之前 Nginx 配置文件的处理方式是类似的。

```
files = /home/yangxg/etc/supervisor/conf.d/*.ini
```

然后我们到 conf.d 新建我们博客应用的配置：

```
[program:hellodjango-blog-tutorial]
command=pipenv run gunicorn blogproject.wsgi -w 2 -k gthread -b 127.0.0.1:8000
directory=/home/yangxg/apps/HelloDjango-blog-tutorial
autostart=true
autorestart=unexpected
user=yangxg
stdout_logfile=/home/yangxg/etc/supervisor/var/log/hellodjango-blog-tutorial-stdout.log
stderr_logfile=/home/yangxg/etc/supervisor/var/log/hellodjango-blog-tutorial-stderr.log
```

说一下各项配置的含义：

[program:hellodjango-blog-tutorial] 指明运行应用的进程，名为 hellodjango-blog-tutorial。

command 为进程启动时执行的命令。

directory 指定执行命令时所在的目录。

autostart 随 Supervisor 启动自动启动进程。

autorestart 进程意外退出时重启。

user 进程运行的用户，防止权限问题。

stdout_logfile，stderr_logfile 日志输出文件。

启动 Supervisor

```
yangxg@server:$ supervisord -c ~/etc/supervisord.conf
```

-c 指定 Supervisr 启动时的配置文件。

进入 supervisorctl 进程管理控制台：

```
yangxg@server:$ supervisorctl -c ~/etc/supervisord.conf
```

执行 update 命令更新配置文件并启动应用。

浏览器输入域名，可以看到服务已经正常启动了。