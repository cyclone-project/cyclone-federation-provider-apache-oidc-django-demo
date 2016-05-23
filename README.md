# cyclone-federation-provider-apache-oidc-django-demo
A demonstration on how to authentified a user in django using the CYCLONE federation provider with Apache 2 and mod_oidc


## How to run:

```shell


# Build with (docker)[https://www.docker.com]
./build.sh

# Run 
./run.sh


```

## Known problem

If you encounter an error 100 during the build with the apt-get update, it can means that you are behind a firewall that is blocking some dns resolution. To fix it, use your in-house dns like this :


```shell

# Build with (docker)[https://www.docker.com] behind a firewall
docker --dns 157.136.10.1 --dns 157.136.10.2 build -t cyclone/apache2:ssl .

```
