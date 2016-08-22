## Stage34
Freescale Staging Environment


## Webapp
#### Required
- Python 2.7
- Redis Server

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

## Worker
#### Python Packages
```
$ cd worker
$ pip install requirements/dev.txt
```

#### Run Celery Worker
```
$ ENV=local python app.py worker -B --loglevel=info -Q q_default
```

## Nginx
```
$ nginx -p nginx -c nginx.conf
```
