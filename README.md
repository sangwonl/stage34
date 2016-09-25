## Stage34
Freescale Staging Environment
** Local Dev Environment Only (for now) **

![alt tag](http://g.recordit.co/0J84vWlwC5.gif)


## Required
### For Webapp (with Celery)
- Python 2.7
- Redis Server (Broker & Result Backend)
- Docker & Docker Compose

### Frontend
- npm 3.x.x
- node 4.x.x


#### Prerequisite
If you are in local environment,

- need to add STAGE34_HOST(defined in `main.settings` and it is `stage34.io` by default) into `/etc/hosts`
- need to make your group to skip password for sudo specific command so that stage34 app can access and modify `/etc/hosts`. Open sudoer configuration by `sudo visudo` and add followings.
```
Cmnd_Alias  STAGE34_HOST_UPDATER = <stage34-project-home>/etc/scripts/host_updater.sh
%staff  ALL=(ALL) NOPASSWD: STAGE34_HOST_UPDATER
```
- need to add a new github 3rd-party application and update `settings.GITHUB_API` with client id and secret.

#### Step1 - Python Packages
```
$ cd webapp
$ pip install requirements/dev.txt
```

#### Step2 - Migration
```
$ ENV=local python manage.py migrate
```

#### Step3 - Run Server
```
$ ENV=local python manage.py runserver 0.0.0.0:8080
```

#### Step4 - Run Celery Worker
```
$ ENV=local celery -A main worker -B --loglevel=info -Q q_default
```
or
```
$ ENV=local python main/celeryworker.py worker -B --loglevel=info -Q q_default
```


#### Step5 - Node Modules
```
$ npm install
```

#### Step6 - Serve App with Watch
```
$ npm start
```

#### Step7 - Nginx
```
$ nginx -p nginx -c nginx.conf
```

#### Step8 - Open 'http://stage34.io:8000'
