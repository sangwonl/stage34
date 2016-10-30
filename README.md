## Stage34
Freescale Staging Environment

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
#### GitHub Application
- need to add a new github 3rd-party application and update `settings.GITHUB_API` with client id and secret.

#### Local DNS Resolving
if local test environment, it's recommended to use `Dnsmasq` to resolve local subdomain.

- Mac OS X
```
# Install it
$ brew install dnsmasq

# Create the etc dir if needed
$ mkdir -p /usr/local/etc

# Create a simple configuration
$ echo "address=/.stage34.io/0.0.0.0" > /usr/local/etc/dnsmasq.conf

# Install the daemon startup file
$ sudo cp -fv /usr/local/opt/dnsmasq/*.plist /Library/LaunchDaemons

# Start the daemon
$ sudo launchctl load /Library/LaunchDaemons/homebrew.mxcl.dnsmasq.plist

$ sudo mkdir -p /etc/resolver
$ sudo sh -c 'echo "nameserver 0.0.0.0" > /etc/resolver/stage34.io'

$ ping sub.stage34.io
```

- Ubuntu
```
$ sudo nano /etc/NetworkManager/NetworkManager.conf
- search for "dns=dnsmasq"
- replace with "#dns=dnsmasq"

$ sudo apt-get install dnsmasq
$ sudo nano /etc/dnsmasq.conf
- append line: "listen-address=0.0.0.0"
- append line: "bind-interfaces"
- append line: "address=/.stage34.io/0.0.0.0"

$ sudo netstat -plant | grep :53
- look for "NUMBER/dnsmasq"
$ sudo kill -9 NUMBER
- fill in the number you found for "NUMBER"

$ sudo service dnsmasq restart
$ sudo nano /etc/dhcp/dhclient.conf
- append line: "prepend domain-name-servers 0.0.0.0;"

$ sudo service network-manager restart
```

References)
http://asciithoughts.com/posts/2014/02/23/setting-up-a-wildcard-dns-domain-on-mac-os-x/
https://www.leaseweb.com/labs/2013/08/wildcard-dns-ubuntu-hosts-file-using-dnsmasq/


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
