# Исследовательский проект влияния новостей на предсказание цен.
## Сборка датасета новостей

### Скрипт для асинхронной обкачки урлов
Например, 10 одновременных запросов могут задаваться командой:

```bash
python3 main.py urls.txt -c 10
```

Для отладочного режима флаг `--debug`

```bash
python3 main.py urls.txt -c 10 --debug
```

### Шаблон файла urls.txt:

source_id category_id supercategory_id url

#### Например

Yahoo Investments CSCO https://finance.yahoo.com/some_path?p=param


#### При парсинге:
- source_id влияет на функцию, которая будет вызвана для получения новости с url
- category_id никак не учитывается
- company_ticker_id никак не учитывается


#### Для формирования парсером списка url
```bash
python3 yahoo_parser.py
```