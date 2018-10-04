# GeoGIF
The GeoGIF server provides users a simple web form to create animations from time-enabled WMS sources in the animated GIF and movie formats
# Requirements

Requirements to use GeoGIF:
* Python 3.4 with virtualenv and pip installed
* ubuntu 14 + or mageia 6 +

# Installation

Clone GeoGIF locally on your filesystem.

```git clone https://github.com/Gabriel-Desharnais/GeoGIF.git```

To install GeoGIF run:

```
cd GeoGIF
/bin/bash setup.sh
```

# Running 

## With a front end

To start GeoGIF front-end run:

```
. GGcontroller/startTestServer.sh
```

Access the URL path with a web browser.

1. You must add the WMS server you want to use in the ```sourceDB``` page. 
 * Base map example: http://www.gebco.net/data_and_products/gebco_web_services/web_map_service/mapserv 	
 * Meteorological data example: http://geo.weather.gc.ca/geomet-beta
2. Update the WMS server so that the Time extent values will be valid
3. Go to ```GEOGIF1``` page and fill the form

## From the command line

In GeoGIF folder, use command line: 
```
GeoGIF/GeoGIF.py <input yaml> <output folder>
```

Where:
* ```input yaml```: the desired configuration, see the Configuration section
* ```output folder```: destination of the output animated GIF

# Configuration

Refer to the [auto-documented sample yaml configuration file](doc/geogif-configuration.yml).

# Test

You can test GeoGIF backend by running it with the sample configuration: 
```
python GeoGIF/GeoGIF.py example/geogif-configuration.yml .
```

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
