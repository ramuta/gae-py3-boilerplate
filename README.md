# GAE Py3 Boilerplate

A web application starter for Google App Engine Python 3 runtime.

> If you like this project, please **star it**! ;) 

## Features

- **Different types of authentication system:**
  - Email-only auth (password-less, login is via emailed magic link)
  - Email/password authentication
- **Translations:**
  - In-built simple translation system
  - Each language has its own templates folder
- **Emailing system**: via SendGrid
- **Various access levels:** public, basic user, admin. Other levels can be easily added using decorators.
- **CSRF protection**
- **Background tasks**
- **Cron jobs**
- **Datastore**: NoSQL database with a very generous free tier and great scalability.
- **Tests**

## Quickstart

1. **Run** the web app using `run.py` ([instructions](docs/run-web-app.md)).
2. **Initialize** the web app via `http://localhost:8080/init`. You can enter fake SendGrid key in the beginning ([instructions](docs/init.md)).
3. **Login** with your email and find the magic login link in the Terminal (in the printed email message). Click on the link and you'll be logged in.
4. **Explore** the web app: `/profile`, `/admin/users` etc.

## Documentation

- [Set up local development environment](docs/environment.md)
- [How to run the web app](docs/run-web-app.md)
- [Web app initialization (important!)](docs/init.md)
- [Load fake data (for localhost usage)](docs/load-fake-data.md)
- [How to run tests](docs/tests.md)
- [Decorators](docs/decorators.md)
- [Handlers: how to create and use them (controllers/views)](docs/handlers.md)
- [Translation system](docs/translations.md)
- [See the data in Datastore visually on localhost](docs/datastore-visually-localhost.md)
- [Background tasks](docs/background-tasks.md)
- [Cron jobs](docs/cron-jobs.md)
- [Deployment](docs/deployment.md)

## TODO

- When a user logs in, send an email to the user with the info about the session (IP, platform, country)
- Admin: when admin changes some user's email address, also delete all the user's session tokens
- User change email: 
    - in a similar way as reset password works
    - BUT, it only changes, if the user clicks verification link on the new email address
    - in this case, the token hash is made out of token + new email address
    - additional security measure: when user changes email address, the password should be set to some random password (so the user is forced to reset it again)
    - also, delete all sessions for that user
- Admin: update SendGrid key
- User: upload profile picture to Google Cloud Storage
- Slovene translations (all HTML templates)
- Documentation

## Known issues

- ...
