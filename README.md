## Stage34
Freescale Staging Environment


## Webapp
### Required
- Python 2.7
- Redis

### Migration
```
$ ENV=local python manage.py migrate
```

### Run Server
```
$ ENV=local python manage.py runserver
```

## Frontend
### Required
- npm 3.x.x
- node 4.x.x

### Node Modules
```
$ npm install
```

### Serve App with Watch
```
$ npm start
```

### Build App
```
$ npm run build
```
