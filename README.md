## Stage34
Freescale Staging Environment
** Local Dev Environment Only (for now) **

![alt tag](http://g.recordit.co/0J84vWlwC5.gif)

## Docker Container Structure

                    +-------+       +--------+  +-------+  +--------+
          +---------+ Nginx +-------+ Webapp +--+ Redis +--+ Worker +---+
          |         +--+----+       +----+---+  +-------+  +--+-----+   |
          |            |  +----------+  |                     |         |
          |            |  | Frontend |  |                     | /var/run/docker.sock
          |            |  +----+-----+  |                     |         |
          |            |       |        |                     |         |
          |         +--+-------+--------+---------------------+-----+   |
    +-----+-----+   |    /etc/nginx/                                |   |
    |   Stage   |   |    /usr/stage34/db/                           |   |
    | Container |   |    /usr/stage34/assets/                       |   |
    +-----------+   |    /usr/stage34/frontend/                     |   |
                    |    /usr/stage34/repo/                         |   |
                    +-----------------------------------------------+   |
                    |                 Volume Container              |   |
                    +-----------------------------------------------+   |
                                                                        |
                    +-----------------------------------------------+   |
                    |                    Docker Host                +---+
                    +-----------------------------------------------+

## Required
- Docker & Docker Compose
- Python 2.7
- npm 3.x.x
- node 4.x.x


## Prerequisite
- need to add a new github 3rd-party application and update `settings.GITHUB_API` with client id and secret.

## Build
#### Frontend
```
$ cd frontend
$ npm install
$ npm run build
```

#### Django Migrate
```
$ cd webapp
$ pip install -r requirements/prod.txt
$ python manage.py migrate
```

## Run
```
$ docker-compose up
```
