## 3. Docker

**Результат:** сервис запускается в контейнере от непривилегированного пользователя.

Создайте Dockerfile:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY app.py .
USER 65532:65532
EXPOSE 8080
CMD ["python", "-u", "app.py"]
```

```bash
docker build -t devops-lab:local .
docker run --rm -d --name devops-lab -p 127.0.0.1:8080:8080 devops-lab:local
curl -i http://127.0.0.1:8080/healthz
docker logs devops-lab
docker inspect --format '{{.Config.User}}' devops-lab
docker stop devops-lab
```

**Проверка:** ответ 200, пользователь контейнера 65532:65532, после stop контейнер удалён. Если порт занят, остановите только свой учебный сервис или поменяйте внешний порт. **Поломка:** запустите без `-p` и объясните, почему запрос с хоста не работает. Для реальной поставки фиксируйте базовый образ по digest и регулярно обновляйте его.


***

создал докерфайл, закоммитил
```Dockerfile
FROM python:3.13-slim
WORKDIR /app
USER 65532:65532
EXPOSE 8080
CMD ["python", "-u", "app.py"]

COPY app.py .
```
сместил инструкцию COPY вниз, так сборка новых образов будет быстрее

```shell
$ docker build -t http-server:local . # -t for naming image in "name:tag" format
$ docker run --rm -d --name http-server -p 127.0.0.1:8080:8080 http-server:local
$   # --rm will remove conainer after stop
$   # -d means that container will be daemonized
$ docker ps
CONTAINER ID   IMAGE               COMMAND              CREATED         STATUS         PORTS                      NAMES
dadd6b142d28   http-server:local   "python -u app.py"   6 seconds ago   Up 5 seconds   127.0.0.1:8080->8080/tcp   http-server

$ curl localhost:8080/healthz
{"status": "ok"}

$ curl localhost:8080
{"service": "devops-lab", "version": "local"}

$ docker inspect --format '{{.Config.User}}' http-server
65532:65532

$ docker logs http-server
172.17.0.1 - - [05/Nov/2026 14:37:23] "GET / HTTP/1.1" 200 -

$ docker stop http-server
http-server
```


без проброса портов до сервера будет не достучатся, потому что он спрятан за NAT докера
наш хост имеет прямой доступ в локальную сеть докера, так что можно провернуть следующую махинацию:
```bash
$ docker run --rm -d --name http-server http-server:local
18f243699d0b29a22ffe9ccc19e75e07a6edd7885f8944d96fa136d2cfa97fb5

$ curl 127.0.0.1:8080
curl: (7) Failed to connect to 127.0.0.1:8080 after 0 ms: Could not connect to server

$ curl 172.17.0.2:8080
{"service": "devops-lab", "version": "local"}
```
