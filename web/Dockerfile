# Use ubuntu image
FROM ubuntu:18.04

#Update
RUN apt-get -yqq update
#Install apache quiet and say yes to everything
RUN apt-get install -yqq apache2 apache2-utils libapache2-mod-wsgi-py3 python3 python3-pip net-tools wget


# Import requirements
copy ./GeoGIF/ /var/www/GeoGIF


RUN pip3 install -U pip
RUN pip3 install requests
RUN pip3 install -r /var/www/GeoGIF/requirements.txt

# set imageio folder
RUN mkdir /usr/imageio/
RUN chown www-data /usr/imageio/

RUN echo "export IMAGEIO_USERDIR=/usr/imageio/" >> /etc/apache2/envvars

# Create DB and migrate models and static stuf
RUN cd /var/www/GeoGIF/FrontEnd/ ; python3 manage.py makemigrations
RUN cd /var/www/GeoGIF/FrontEnd/ ; python3 manage.py migrate
RUN cd /var/www/GeoGIF/FrontEnd/ ; python3 manage.py collectstatic
# Allow read and write on db
RUN chown -R www-data /var/www/GeoGIF/FrontEnd/

copy ./web/apache2.conf /etc/apache2/apache2.conf

# Get ip
# Start apache
# Add geomet and update the source in db
RUN cd /var/www/GeoGIF/FrontEnd/; python3 manage.py runserver localhost:8000 & sleep 10; wget "http://localhost:8000/AddSource/?source=http%3A%2F%2Fgeo.weather.gc.ca%2Fgeomet%2F&name=geomet" ; wget "http://localhost:8000/updateASource/?source=http%3A%2F%2Fgeo.weather.gc.ca%2Fgeomet%2F"
CMD cd /var/www/GeoGIF/FrontEnd/ ; daphne -p 8001 -b "$(ifconfig | grep -A 1 'eth0' | tail -1 | grep -o 'inet.*netmask' | grep -o [0-9.]*)" FrontEnd.asgi:application & apachectl -D FOREGROUND
