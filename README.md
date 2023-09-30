### Simple start

- ```$ cp .env.backend .env```
- ```$ cp .env.frontend frontend/.env.local```
- ```$ docker-compose up```

### Create initial operator

- ```$ docker exec -it csms-manager-thnxel python backend/commands/create_operator.py --email <email> --password <password>```