# Use ubuntu image
FROM ubuntu:18.04

#Update
RUN apt-get -yqq update
#Install apache quiet and say yes to everything
RUN apt-get install -yqq apache2 apache2-utils libapache2-mod-wsgi-py3 python3 python3-pip net-tools


# Import requirements
copy ./GeoGIF/ /var/www/GeoGIF


RUN pip3 install -U pip
RUN pip3 install -r /var/www/GeoGIF/requirements.txt

# set imageio folder
RUN mkdir /usr/imageio/
RUN chown www-data /usr/imageio/
RUN chown -R www-data /var/www/GeoGIF/FrontEnd/
RUN echo "export IMAGEIO_USERDIR=/usr/imageio/" >> /etc/apache2/envvars


copy ./apache2.conf /etc/apache2/apache2.conf

# Get ip
# Start apache
CMD cd /var/www/GeoGIF/FrontEnd/ ; daphne -p 8001 -b "$(ifconfig | grep -A 1 'eth0' | tail -1 | grep -o 'inet.*netmask' | grep -o [0-9.]*)" FrontEnd.asgi:application & apachectl -D FOREGROUND
