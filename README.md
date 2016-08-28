## Stage34
Freescale Staging Environment


## Webapp (with Celery)
#### Required
- Python 2.7
- Redis Server (Broker & Result Backend)

#### Python Packages
```
$ cd webapp
$ pip install requirements/dev.txt
```

#### Migration
```
$ ENV=local python manage.py migrate
```

#### Run Server
```
$ ENV=local python manage.py runserver 0.0.0.0:8080
```

#### Run Celery Worker
```
$ ENV=local celery -A main worker -B --loglevel=info -Q q_default
```
or
```
$ ENV=local python -m main.worker worker -B --loglevel=info -Q q_default
```


## Frontend
#### Required
- npm 3.x.x
- node 4.x.x

#### Node Modules
```
$ npm install
```

#### Serve App with Watch
```
$ npm start
```

#### Build App
```
$ npm run build
```


## Nginx
```
$ nginx -p nginx -c nginx.conf
```
