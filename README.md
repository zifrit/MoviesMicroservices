### 3 Микросервиса 
1. Сервис авторизации (**auth**)
2. Сервис с фильмами (**movies**)
3. Сервис с комментариями (**comments**)

Для запуска проекта нужно сделать следующее:
1. Клонируйте проект себе на компьютер:
```bash
git clone https://github.com/zifrit/MoviesMicroservices.git
```
2. Генерация приватного (**jwt-private.pem**) и публичного (**jwt-private.pem**) ключей:
```bash
openssl genrsa -out jwt-private.pem 2048 && openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```
3. Запуск проекта в докере 
```bash
docker compose -f docker-compose.yaml up --build -d
```
В докере поднимается postgres:15-alpine, 3 сервиса, nginx и redis. 
При запуске postgres создаются базы для каждого сервиса, в **init-db/init-database.sh** прописаны команды для создания этих таблиц
Redis, служит для хранения черного списка токенов которые разлогинены.

#### Документация будет доступна по адресу 
- для сервиса auth http://app_host/auth/api/openapi
- для сервиса comments http://app_host/comments/api/openapi
- для сервиса movies http://app_host/movies/api/openapi
