### The application's internals described [here](https://docs.google.com/document/d/1creKl0rNEWSN2G-6Wucqz96a-7sLhqn5fX9o02pi1GI/edit?usp=sharing).

### Simple start

- ```$ cp .env.backend .env```
- ```echo GITHUB_TOKEN=<token> >> .env```
- ```$ cp .env.frontend frontend/.env.local```
- ```$ docker-compose up --build -d```

- ```echo -e '$d\nw\nq'| ed .env```

- ```docker exec -it ocpp-manager stripe login --interactive --project-name <project name>```
- ```docker exec -it -d ocpp-manager stripe listen --forward-to "http://localhost:<port>/stripe-webhook"```

### Create initial operator

- ```$ docker exec -it ocpp-manager python backend/commands/create_operator.py --email <email> --password <password> --fname <first name> --lname <last name> --address <address>```