FROM centos:7

# httpd installation
RUN yum update -y && yum install -y httpd mod_ssl mod_wsgi nano && yum clean -y all

# mod_auth_openidc installation
RUN yum update -y && yum install -y epel-release && yum -y --nogpgcheck localinstall https://github.com/pingidentity/mod_auth_openidc/releases/download/v1.8.8/mod_auth_openidc-1.8.8-1.el7.centos.x86_64.rpm && yum clean -y all

# pip install
RUN yum update -y && yum install -y epel-release python-pip && yum clean -y all

# Installing the requirements of the project
ADD ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copying SSL certificate
COPY ./apache2/ /etc/apache2/
RUN chown -R apache:apache /etc/apache2/* && chmod 440 -R /etc/apache2/*

# To make a django server with openid protecting everything

#COPY ./apache_groups /etc/apache2/apache_groups

COPY ./django-openid.conf /etc/httpd/conf.d/django-openid.conf

CMD cd /var/www/django && python manage.py collectstatic --no-input && /usr/sbin/apachectl -DFOREGROUND

EXPOSE 443
EXPOSE 80
