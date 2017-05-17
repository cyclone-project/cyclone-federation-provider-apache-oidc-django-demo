source settings.conf
export PROJECT_ROOT=$(cd $PROJECT_ROOT; pwd)
export HTTPD_LOG_ROOT=$(cd $HTTPD_LOG_ROOT; pwd)
if [ "$1" == "" ]
then
	DEAMON_OR_NOT=d
else
	DEAMON_OR_NOT=it
fi


if [ ! -e restore_rights.sh ]
then
	echo "#!/bin/bash">restore_rights.sh
	echo "chmod $(stat -c%a $PROJECT_ROOT) $PROJECT_ROOT" >> restore_rights.sh
	echo "chmod $(stat -c%a $DB_LOCATION) $DB_LOCATION" >> restore_rights.sh
fi

chmod a+x+w $PROJECT_ROOT
chmod a+w $DB_LOCATION

mkdir -p /tmp/${STATIC_URI}
mkdir -p /ifb/${MEDIA_URI}
chmod -R 777 /ifb/${MEDIA_URI}

docker run -${DEAMON_OR_NOT} -p $HTTPS_PORT_HOST:443 -p $HTTP_PORT_HOST:80 -e FQDN=${FQDN} -e PROJECT_NAME=${PROJECT_NAME} -e MEDIA_URI=${MEDIA_URI} -e STATIC_URI=${STATIC_URI} -e OIDC_URI=${OIDC_URI} -v /ifb/${MEDIA_URI}:/var/www/django/${MEDIA_URI} -v /tmp/${STATIC_URI}:/var/www/django/${STATIC_URI} -v $DB_LOCATION:/var/www/django/usecases.db -v ${PROJECT_ROOT}:/var/www/django -v ${HTTPD_LOG_ROOT}:/var/log/httpd -v /etc/localtime:/etc/localtime:ro --name django ${DOCKER_IMAGE_OWNER}/${DOCKER_IMAGE_NAME}:latest $1 $2 $3 $4 $5 $6 $7 $8 $9

