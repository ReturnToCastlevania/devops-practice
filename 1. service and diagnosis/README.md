# Задание
## 1. Сервис и диагностика
**Результат:** локальный HTTP-сервис и понимание, как найти его процесс и порт.

Создайте папку и файл app.py:

```python
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/healthz':
            body, status = {'status': 'ok'}, 200
        elif self.path == '/':
            body, status = {'service': 'devops-lab', 'version': os.getenv('APP_VERSION', 'local')}, 200
        else:
            body, status = {'error': 'not found'}, 404
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
```

Запустите `python3 app.py` в одном терминале, а в другом выполните:

```bash
curl -i http://127.0.0.1:8080/healthz
curl -i http://127.0.0.1:8080/missing
lsof -i :8080
```

**Проверка:** первый запрос возвращает 200 и JSON, второй - 404. Найдите PID процесса и остановите сервер через Ctrl+C. Если порт занят, найдите владельца порта; не завершайте неизвестный процесс.

**Поломка:** остановите сервер и повторите curl. Чем ошибка соединения отличается от HTTP 404? Запишите ответ. Дополнительно добавьте тест неизвестного маршрута и переменной APP_VERSION.


# Практика
## запуск сервера
```bash
python app.py
# сервер молчит - значит работает
```

## проверка сервера
```bash
# флаг -i в curl показывает http заголовки
$ curl -i localhost:8080/
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.13.17
Date: Wed, 04 Nov 2026 11:32:50 GMT
Content-Type: application/json
Content-Length: 45

{"service": "devops-lab", "version": "local"}



$ curl -i localhost:8080/healthz
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.13.17
Date: Wed, 04 Nov 2026 11:33:20 GMT
Content-Type: application/json
Content-Length: 16

{"status": "ok"}



$ curl -i localhost:8080/missing
HTTP/1.0 404 Not Found
Server: BaseHTTP/0.6 Python/3.13.17
Date: Wed, 04 Nov 2026 11:33:24 GMT
Content-Type: application/json
Content-Length: 22

{"error": "not found"}
```

## логи сервера
```logs

127.0.0.1 - - [04/Nov/2026 14:32:50] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [04/Nov/2026 14:33:20] "GET /healthz HTTP/1.1" 200 -
127.0.0.1 - - [04/Nov/2026 14:33:24] "GET /missing HTTP/1.1" 404 -
```


## выключение сервера
```bash
$ lsof -i :8080
COMMAND  PID USER FD   TYPE DEVICE SIZE/OFF NODE NAME
python  6887 pled 3u  IPv4 113878      0t0  TCP *:http-alt (LISTEN)
$ kill -2 6887   # штатное прерываное программы
```




## **Поломка:** остановите сервер и повторите curl. Чем ошибка соединения отличается от HTTP 404? Запишите ответ. 
```bash
$ # сервер работает
$ curl -i localhost:8080/12
HTTP/1.0 404 Not Found
Server: BaseHTTP/0.6 Python/3.13.17
Date: Wed, 04 Nov 2026 11:58:42 GMT
Content-Type: application/json
Content-Length: 22

{"error": "not found"}

$ kill -2 $(lsof -i :8080 | tail -n 1 | awk '{print $2}')
$ # сервер выключен
$ curl -i localhost:8080/12
curl: (7) Failed to connect to localhost:8080 after 0 ms: Could not connect to server
```
* ошибка соединения не имеет http заголовков, убо происходит до отправки запроса, а также происходит на другом слою модели tcp/ip - транспортном (понятие соединения вводится протоколом TCP, нижестоящие протоколы просто отправляют данные)



## Дополнительно добавьте тест неизвестного маршрута и переменной APP_VERSION.
* что такое тест неизвестного маршрута я не понял

### тест переменной APP_VERSION
```bash
$ APP_VERSION=1356 python app.py
```
```bash
$ curl -i localhost:8080
HTTP/1.0 200 OK
Server: BaseHTTP/0.6 Python/3.13.17
Date: Wed, 04 Nov 2026 12:58:54 GMT
Content-Type: application/json
Content-Length: 44

{"service": "devops-lab", "version": "1356"}
```
работает


