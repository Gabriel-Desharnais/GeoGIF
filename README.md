# GeoGIF
The GeoGIF server provides users a simple web form to create animations from time-enabled WMS sources in the animated GIF and movie formats
# Requirements

Requirements to use GeoGIF:
* Python 3.4 with virtualenv and pip installed
* ubuntu 14 + or mageia 6 +

# Installation

Clone GeoGIF locally on your filesystem.

You can start the container with
```
docker-compose build
docker-compose up
```
The server is now running on port 80

It should give an image like the one below:

![alt text](https://raw.githubusercontent.com/gabriel-desharnais/GeoGIF/master/example/geogif-output.gif)


# To do
- [x] Download images from WMS request
- [x] Generate GIFs
- [x] Generate different video format
- [x] Output GIFs and videos to a web page
- [x] Create a online form to request generation of GIFs
- [x] Have a working webapp
- [ ] Create an API to make it eassy for other app to request GIFs from a GeoGIF server
- [ ] Add a parameter to have a time stamp displayed on images
- [ ] Enhance the visual aspect of the lower banner
