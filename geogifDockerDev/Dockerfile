# Use ubuntu image
FROM ubuntu:18.04

#Update
RUN apt-get -yqq update
#Install apache quiet and say yes to everything
RUN apt-get install -yqq python3 python3-pip

# Import requirements
COPY ./GeoGIF/ /var/www/GeoGIF


RUN pip3 install -U pip
RUN pip3 install requests
RUN pip3 install -r /var/www/GeoGIF/requirements.txt

# set imageio folder
RUN mkdir /usr/imageio/
WORKDIR /var/www/GeoGIF/FrontEnd/
EXPOSE 8000
ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
