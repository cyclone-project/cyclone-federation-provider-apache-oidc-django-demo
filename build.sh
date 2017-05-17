source settings.conf
export PROJECT_ROOT=$(mkdir -p $PROJECT_ROOT ; cd $PROJECT_ROOT ; pwd)
export HTTPD_LOG_ROOT=$(mkdir -p $HTTPD_LOG_ROOT ; cd $HTTPD_LOG_ROOT; pwd)
#envsubst < "Dockerfile.template" > "Dockerfile.generated"
#envsubst < "docker-compose.template.yml" > "docker-compose.yml"
cp ${PROJECT_ROOT}/requirements.txt ./requirements.txt
docker ${DNS_FOR_DOCKER} build -t ${DOCKER_IMAGE_OWNER}/${DOCKER_IMAGE_NAME}:${TAG} -t ${DOCKER_IMAGE_OWNER}/${DOCKER_IMAGE_NAME}:latest -f Dockerfile .
rm ./requirements.txt
echo "Image built : ${DOCKER_IMAGE_OWNER}/${DOCKER_IMAGE_NAME}:${TAG}"
echo "Image built : ${DOCKER_IMAGE_OWNER}/${DOCKER_IMAGE_NAME}:latest"
