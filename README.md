![FASTAPI](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)
# Property Managment API
> Backend of property managment api, which it's goal it's to manage properties, and users of it's platform.



## Installation

Docker & docker-compose 
```sh
git clone https://github.com/vjanz/property-managment-platform.git
```
<br>
After cloning, get inside the project, and create .env and update with the values from .env.example

Build and run services: (web api, postgres database and pgadmin with docker-compose)
```sh
docker-compose up -d 
```
<br>
After the built is done, and the services are running, get inside the api container, run the migrations and create the superuser

```sh
docker exec -it property-api bash
make migrate
make init-data
```
After this step you should be good to go.

## API
![alt text](https://i.imgur.com/9POaBZj.png)

## Project Structure

    src
    └── alembic               - database migrations
        └── flex              - source code root
             ├── auth         - authentication related module
             ├── core         - settings, common functions, enums, security, i18n etc
             ├── db           - base, dependencies, mixins, sessions
             ├── property     - Everything(models, schemas, dependencies, api, service) related to property module
             ├── user         - Everything(models, schemas, dependencies, api, service) related to user module
        
Basically, everything related to a resource is grouped in a single package. 
If for example we have a new feature ex: Payments, there would be a new directory that holds all the logic
related to that module.
## 

Valon – [Valon Januzaj](https://www.linkedin.com/in/valon-januzaj-b02692187/) <br>valon.januzaj98@gmail.com<br>
[https://github.com/vjanz](https://github.com/vjanz/)
