## 4. Compose и состояние

**Результат:** приложение и Redis общаются по внутренней сети, данные переживают пересоздание контейнера. Это отдельная учебная проверка хранилища: приложение пока не использует Redis.

Создайте compose.yaml:

```yaml
services:
  app:
    build: .
    ports:
      - "127.0.0.1:8080:8080"
    environment:
      APP_VERSION: compose
  redis:
    image: redis:7-alpine
    command: ["redis-server", "--appendonly", "yes"]
    volumes:
      - redis-data:/data
volumes:
  redis-data:
```

```bash
docker compose up -d --build
curl http://127.0.0.1:8080/
docker compose exec redis redis-cli SET course hello
docker compose down
docker compose up -d
docker compose exec redis redis-cli GET course
```

**Проверка:** версия compose, GET возвращает hello. `docker compose down` сохраняет том; `docker compose down -v` удалит учебные данные и выполняется только после проверки.
**Поломка:** сравните имя сервиса redis с localhost внутри контейнера. Почему localhost указывает на сам контейнер? Пароли и реальные данные в этот пример не помещайте.

***

```shell
$ docker compose up -d --build

$ curl 127.0.0.1:8080
{"service": "devops-lab", "version": "compose"}

$ docker compose exec redis redis-cli SET hello world
OK

$ docker compose exec redis redis-cli GET hello
"world"

$ docker compose down

$ docker compose exec redis redis-cli GET hello
"world"

$ docker compose down -v # -v removes volumes

$ docker volume ls
DRIVER    VOLUME NAME

$ docker compose up -d
[+] up 4/4
 ✔ Network devops-practice_default   Created                                   0.1s
 ✔ Volume devops-practice_redis-data Created                                   0.0s
 ✔ Container devops-practice-redis-1 Started                                   0.8s
 ✔ Container devops-practice-app-1   Started                                   0.8s

$ docker volume ls
DRIVER    VOLUME NAME
local     devops-practice_redis-data

$ docker compose exec redis redis-cli GET hello
(nil)
```


> **Поломка:** сравните имя сервиса redis с localhost внутри контейнера. Почему localhost указывает на сам контейнер?
```bash
/data # ping -c 1 localhost | head -1
PING localhost (::1): 56 data bytes
/data # контейнер имеет собственный loopback-интерфейс, убо он находится в изолированном неймспейсе

/data # ping -c 1 redis | head -1
PING redis (172.18.0.3): 56 data bytes

/data # ping -c 1 app | head -1
PING app (172.18.0.2): 56 data bytes
/data # # контейнеры находятся в одной сети и досягаемы друг до друга
```

