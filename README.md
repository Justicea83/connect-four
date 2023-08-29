# Testing the application

## Running the application

Ensure both docker and docker-compose are installed on your local machine or vm.

### Run the following commands:
- Rename `.env.example` to `.env` in the backend directory
- `docker-compose up -d --build` in the root directory
- The web application should be running on port 3000 of you host machine. (Eg. http://localhost:3000)
- The API application should be running on port 8000 of you host machine. (Eg. http://localhost:8000)
- You should see a swagger UI on the root route of your the API application.

## Running the tests
For API, Run `docker-compose run --rm api sh -c "python manage.py test"`

For WEB
Run:
- `npm install` in the `/frontend` directory
- `npm test`

### Default Login Credentials for the 2 game players

```json
{
  "username": "frank",
  "password": "secret",
}
```

```json
{
  "username": "james",
  "password": "secret",
}
```

## Postgres Adminer
The postgres adminer is running on port 5050 of your local machine with this login details:
```json
{
  "username": "admin@example.com",
  "password": "admin"
}
```

### To add a server, use this details:
Name: [Any Name At all]

On the `connection` tab, use this details:
```json
{
    "host": "db",
    "port": 5432,
    "maintenanceDatabase": "postgres",
    "username": "sail",
    "password": "password"
}
```

After creating the server, you can find the tables on the left pane.

<img width="525" alt="Screenshot 2023-08-29 at 06 51 59" src="https://github.com/Justicea83/monadical-test/assets/26106822/72179c38-fdd7-4e02-b5bc-a9cccd642b6d">

### Sample Game

https://github.com/Justicea83/monadical-test/assets/26106822/628fb9c1-29ea-4182-820f-1b21683264ce


