## 5. CI

**Результат:** каждый push и pull request запускает тесты и сборку образа. В своём репозитории создайте .github/workflows/ci.yml:

```yaml
name: CI
on: [push, pull_request]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: python -m unittest -v
      - run: docker build -t devops-lab:ci .
```

Отправьте ветку на GitHub и откройте Actions. **Проверка:** оба шага зелёные; намеренно сломанный тест в отдельном коммите делает проверку красной, исправление возвращает её в зелёное состояние
Для production фиксируйте сторонние actions полным SHA, проверяйте зависимости и не передавайте секреты недоверенному коду из pull request.

***

# создание зеркала на github
мой репозиторий хранится на `codeberg.org`, но тамошний CI еще в тестовом варианте
я создам зеркало репозитория на github
```bash
git remote rename origin codeberg
git remote add origin git@github.com:ReturnToCastlevania/devops-practice.git
git push origin main
```
проблема решена - теперь репозиторий есть и на [codeberg](https://codeberg.org/pledx/devops-practice) и на [github](https://github.com/ReturnToCastlevania/devops-practice), где будет проводится CI

***

# работа с ci/cd
добавил .github/workflows/ci.yml, в github тест зеленый

создал ветку 5-ci-broken, изменил статус ответа с 200 на 201
запушил сломанное изменение, тест красный

починил, тест зеленый



