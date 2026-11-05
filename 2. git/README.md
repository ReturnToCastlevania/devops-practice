## 2. Git и проверка изменений
**Результат:** изменение в отдельной ветке и воспроизводимый тест без сторонних библиотек.

```bash
git init
git add app.py
git commit -m 'Add HTTP service'
git switch -c lab-02-tests
```

Создайте test_app.py:

```python
import json
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from app import Handler

class ServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()

    def test_health(self):
        conn = HTTPConnection('127.0.0.1', self.server.server_port, timeout=2)
        try:
            conn.request('GET', '/healthz')
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.read()), {'status': 'ok'})
        finally:
            conn.close()

if __name__ == '__main__':
    unittest.main()
```

Выполните `python3 -m unittest -v`, затем добавьте тест 404. Проверьте `git diff`, закоммитьте изменения и откройте pull request в своём репозитории. **Поломка:** измените ожидаемый статус на 201, убедитесь, что тест падает, и исправьте его. Не коммитьте намеренно сломанный тест.


***

* создал репозиторий на codeberg, склонировал его по приватному ключу
```bash
$ git add '1. service and diagnosis' # add files from folder to stage zone
$ git commit -m "done task 1" # commit everything in stage
$ git switch -c '2-git-tasks' # create branch and switch to it
```

* создал файл test_app.py, закоммитил изменения
```
$ python -m unittest -v
test_health (test_app.ServiceTest.test_health) ... 127.0.0.1 - - [05/Nov/2026 12:45:29] "GET /healthz HTTP/1.1" 200 -
ok
```

* добавил тест на 404 в набор тестов
```python
    def test_missing(self):
        conn = HTTPConnection('127.0.0.1', self.server.server_port, timeout=2)
        try:
            conn.request('GET', '/missing')
            response = conn.getresponse()
            self.assertEqual(response.status, 404)
            self.assertEqual(json.loads(response.read()), {'error': 'not found'})
        finally:
            conn.close()
```


* добавил не рабочий тест
```python
    def test_broken(self):
        conn = HTTPConnection('127.0.0.1', self.server.server_port, timeout=2)
        try:
            conn.request('GET', '/healthz')
            response = conn.getresponse()
            self.assertEqual(response.status, 201)
            self.assertEqual(json.loads(response.read()), {'error': 'not found'})
        finally:
            conn.close()
```

* проверка тестов
```bash
$ python -m unittest -v
test_broken (test_app.ServiceTest.test_broken) ... 127.0.0.1 - - [05/Nov/2026 12:51:34] "GET /healthz HTTP/1.1" 200 -
FAIL
test_health (test_app.ServiceTest.test_health) ... 127.0.0.1 - - [05/Nov/2026 12:51:34] "GET /healthz HTTP/1.1" 200 -
ok
test_missing (test_app.ServiceTest.test_missing) ... 127.0.0.1 - - [05/Nov/2026 12:51:34] "GET /missing HTTP/1.1" 404 -
ok

======================================================================
FAIL: test_broken (test_app.ServiceTest.test_broken)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/pled/code/devops-practice/test_app.py", line 48, in test_broken
    self.assertEqual(response.status, 201)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 200 != 201

----------------------------------------------------------------------
Ran 3 tests in 0.505s

FAILED (failures=1)
```
* убрал сломанный тест



# Pull request
```bash
git push origin 2-git-tasks
```

codeberg.org/pledx/devops-practice > new pr > `2-git-tasks` to `main` > it gave cli instructions

```bash
# получаем изменения из репозитория
git fetch -u origin 2-git-tasks:2-git-tasks
git switch 2-git-tasks

# переключаемся на ветку main, мержим в нее изменения
git switch main
git merge --no-ff 2-git-tasks
git push origin main
```


