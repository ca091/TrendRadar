## 在此目录下执行

```shell
$ docker-compose pull # 拉取镜像
$ docker-compose up -d # 更新镜像并在后台启动
$ docker-compose up -d --build # 强制 Docker Compose 根据我们新创建的 Dockerfile 来构建 file-watcher 镜像
$ docker-compose restart txt2html # 重启镜像
```