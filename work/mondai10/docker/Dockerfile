FROM ubuntu:16.04
RUN apt-get -y  update && apt-get -y upgrade
RUN apt-get -y install build-essential
RUN apt-get -y install wget
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install mysql-server
RUN apt-get -y install apache2 php php-mysql libapache2-mod-php
RUN bash -c "mkdir -p /usr/local/sqli/pub"
RUN bash -c "chown www-data:www-data /usr/local/sqli -R"

ADD ./apache2.conf /etc/apache2/apache2.conf
ADD ./000-default.conf /etc/apache2/sites-enabled/000-default.conf
ADD ./sql.sql /tmp/sql.sql
ADD ./index.php /usr/local/sqli/pub/index.php
ADD ./mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf

ENV APACHE_LOG_DIR=/tmp/
RUN mkdir -p /var/run/mysqld && chown mysql:mysql /var/run/mysqld

CMD ["bash", "-c", "rm -rf /var/lib/mysql && /usr/sbin/mysqld --initialize-insecure && $(/usr/sbin/mysqld & /usr/sbin/apache2 -D FOREGROUND)"]
EXPOSE 80


