
сборка
docker build -t my_fastapi_app .

запуск
docker run -p 8000:8000 my_fastapi_app


Примеры запросов

Получить суммарный трафик по всем клиентам:
http://127.0.0.1:8000/traffic

Фильтр по ID клиента:
http://127.0.0.1:8000/traffic?customer_id=1

Фильтр по периоду времени:
http://127.0.0.1:8000/traffic?start_date=2023-03-01%2016:30:00&end_date=2023-04-01%2012:00:00

Фильтр по IP-адресу:
GET http://127.0.0.1:8000/traffic?ip=192.168.218.159
