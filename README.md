# OpenID-Connect example with Apache2, SSL, the Cyclone Federation Provider and Django

## How to run:

```shell


# Build with (docker)[https://www.docker.com]
./build.sh

# Run on localhost
./run.sh

# Run on a distant server
edit `settings.conf` and FQDN variable
./run.sh


# Stopping and removing ALL container
docker rm -f $(docker ps -aq)


```

Visit `https://localhost`, for the openid-connect example. Once connected visit `https://localhost/polls`

OIDCRemoteUserClaim setting can be used to specify which claim to use to set REMOTE_USER in apache2.

## Known problem

# Error 100 in apt-get update

If you encounter an error 100 during the build with the apt-get update, it can means that you are behind a firewall that is blocking some dns resolution. To fix it, uncomment and adapte `DNS_FOR_DOCKER` variable in `settings.conf`.


# attempt to write a readonly database

Note that httpd inside the container must have execution right on `PROJECT_ROOT`, and rwx on `$PROJECT_ROOT/db.sqlite3`.
