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
$ alembic -c migrations/conf/local.ini revision "add a new column"   # new revision
$ alembic -c migrations/conf/local.ini upgrade heads                 # migrate to heads
$ alembic -c migrations/conf/local.ini downgrade -1                  # backward to the prev one
```

#### Run Server
```
$ ENV=local python app.py
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
