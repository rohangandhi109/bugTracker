## Project Description
This project is a web application to track bugs with user assignment, role management and notification features.
The project has 4 roles
1. System Admin - CRUD access Users, Projects, Tickets
2. Project Manager - Assign tickets, view progress of tickets and projects, get live notification of new tickets
3. Project Developer - Assign tickets, Change ticket status, live notification of new tickets and assigned tickets
4. Project User - create ticket and check status of tickets. 


## Getting Started

### Installing Dependencies

##### Python 3.7

##### To install all the libraries

```bash
pip install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Auth0](https://auth0.com/)

### Database Setup

This project uses Postgres sql, restore a database using the capstone.psql file provided. From the terminal run:

```bash
psql trackbug < trackbug.psql
```

### Setting the environment variables

1. Postgres sql database URL
``` export DATABASE_URL=postgresql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE_NAME> ```

2. Auth0 Domain name
```export AUTH0_DOMAIN=<YOUR_DOMAIN_NAME>```

3. Auth0 API Audience
```export AUTH0_AUDIENCE=<YOUR_API_AUDIENC>```

4. Auth0 client ID
```export AUTH0_CLIENT_ID=<YOUR_CLIENT_ID>```

5. Auth0 client Secret
```export AUTH0_CLIENT_SECRET=<YOUR_CLIENT_SECRET>```

6. Auth0 callback URL
```AUTH0_CALLBACK_URL=<CALLBACK_URL>```


## Running the web application

#### Locally Running the application

```bash
export FLASK_APP=app
flask run --reload

```

## Deployed project on heroku

### URL

https://bugtracker109-stage.herokuapp.com/








