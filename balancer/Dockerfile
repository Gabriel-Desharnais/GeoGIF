# Use ubuntu image
FROM ubuntu:18.04

#Update
RUN apt-get -yqq update
#Install apache quiet and say yes to everything
RUN apt-get install -yqq apache2 apache2-utils

# Activate load balancing module
RUN a2enmod proxy
RUN a2enmod proxy_http
RUN a2enmod proxy_balancer
RUN a2enmod lbmethod_byrequests
RUN a2enmod proxy_wstunnel
RUN a2enmod rewrite

# Use our version of apache2.conf
copy ./apache2.conf /etc/apache2/apache2.conf

# This container will transmit data to the public threw port 80
EXPOSE 80

# Start apache
CMD apachectl -D FOREGROUND
