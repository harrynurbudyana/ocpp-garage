### Simple start

- ```$ cp .env.backend .env```
- ```$ cp .env.frontend frontend/.env.local```
- ```$ docker-compose up --build -d```
- ```docker exec -it ocpp-manager stripe login --interactive --project-name <project name>```
- ```docker exec -it -d ocpp-manager stripe listen --forward-to "http://localhost:<port>/stripe-webhook"```

### Create initial operator

- ```$ docker exec -it ocpp-manager python backend/commands/create_operator.py --email <email> --password <password> --fname <first name> --lname <last name> --address <address>```